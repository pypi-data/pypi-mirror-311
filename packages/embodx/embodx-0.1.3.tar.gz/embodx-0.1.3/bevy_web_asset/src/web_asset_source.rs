use bevy::{asset::io::PathStream, utils::ConditionalSendFuture};
use std::path::{Path, PathBuf};

use bevy::asset::io::{AssetReader, AssetReaderError, Reader};

/// Treats paths as urls to load assets from.
pub struct WebAssetReader {
    /// Option to cache resource.
    pub cache_resource: bool,
    /// Connection type.
    pub connection: WebAssetReaderConnection,
}

impl WebAssetReader {
    fn get_cache_path(&self, path: &Path) -> Option<PathBuf> {
        if self.cache_resource {
            return directories::ProjectDirs::from("", "", "bevy_web_asset").map(|user_dirs| {
                let hash: String = Sha256::digest(path.to_string_lossy().as_bytes())
                    .iter()
                    .fold(String::new(), |mut acc, b| {
                        acc.push_str(&format!("{:02X}", b));
                        acc
                    });

                user_dirs.cache_dir().join(hash)
            });
        }
        None
    }
}

/// Treats paths as urls to load assets from.
pub enum WebAssetReaderConnection {
    /// Unencrypted connections.
    Http,
    /// Use TLS for setting up connections.
    Https,
}

impl WebAssetReaderConnection {
    fn make_uri(&self, path: &Path) -> PathBuf {
        PathBuf::from(match self {
            WebAssetReaderConnection::Http => "http://",
            WebAssetReaderConnection::Https => "https://",
        })
        .join(path)
    }

    /// See [bevy::asset::io::get_meta_path]
    fn make_meta_uri(&self, path: &Path) -> Option<PathBuf> {
        let mut uri = self.make_uri(path);
        let mut extension = path.extension()?.to_os_string();
        extension.push(".meta");
        uri.set_extension(extension);
        Some(uri)
    }
}

#[cfg(target_arch = "wasm32")]
async fn get<'a>(path: PathBuf, _: Option<PathBuf>) -> Result<Box<Reader<'a>>, AssetReaderError> {
    use bevy::asset::io::VecReader;
    use js_sys::Uint8Array;
    use wasm_bindgen::JsCast;
    use wasm_bindgen_futures::JsFuture;
    use web_sys::Response;

    fn js_value_to_err<'a>(
        context: &'a str,
    ) -> impl FnOnce(wasm_bindgen::JsValue) -> std::io::Error + 'a {
        move |value| {
            let message = match js_sys::JSON::stringify(&value) {
                Ok(js_str) => format!("Failed to {context}: {js_str}"),
                Err(_) => {
                    format!(
                        "Failed to {context} and also failed to stringify the JSValue of the error"
                    )
                }
            };

            std::io::Error::new(std::io::ErrorKind::Other, message)
        }
    }

    let window = web_sys::window().unwrap();
    let resp_value = JsFuture::from(window.fetch_with_str(path.to_str().unwrap()))
        .await
        .map_err(js_value_to_err("fetch path"))?;
    let resp = resp_value
        .dyn_into::<Response>()
        .map_err(js_value_to_err("convert fetch to Response"))?;
    match resp.status() {
        200 => {
            let data = JsFuture::from(resp.array_buffer().unwrap()).await.unwrap();
            let bytes = Uint8Array::new(&data).to_vec();
            let reader: Box<Reader> = Box::new(VecReader::new(bytes));
            Ok(reader)
        }
        404 => Err(AssetReaderError::NotFound(path)),
        status => Err(AssetReaderError::Io(
            std::io::Error::new(
                std::io::ErrorKind::Other,
                format!("Encountered unexpected HTTP status {status}"),
            )
            .into(),
        )),
    }
}

#[cfg(not(target_arch = "wasm32"))]
async fn get<'a>(
    path: PathBuf,
    cache_path: Option<PathBuf>,
) -> Result<Box<Reader<'a>>, AssetReaderError> {
    if let Some(cache_path) = cache_path.as_ref() {
        if cache_path.exists() {
            dbg!("cache hit");
            // TODO: fallback to deleting cache if it fails to read, and re-download the file?
            return Ok(Box::new(VecReader::new(fs::read(cache_path)?)));
        }
    }

    use std::future::Future;
    use std::io::Write;
    use std::pin::Pin;
    use std::task::{Context, Poll};
    use std::{fs, io};

    use bevy::asset::io::VecReader;
    use surf::StatusCode;

    #[pin_project::pin_project]
    struct ContinuousPoll<T>(#[pin] T);

    impl<T: Future> Future for ContinuousPoll<T> {
        type Output = T::Output;

        fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
            // Always wake - blocks on single threaded executor.
            cx.waker().wake_by_ref();

            self.project().0.poll(cx)
        }
    }

    let str_path = path.to_str().ok_or_else(|| {
        AssetReaderError::Io(
            io::Error::new(
                io::ErrorKind::Other,
                format!("non-utf8 path: {}", path.display()),
            )
            .into(),
        )
    })?;

    let client = surf::Client::new().with(surf::middleware::Redirect::new(5));
    let mut response = ContinuousPoll(client.get(str_path)).await.map_err(|err| {
        AssetReaderError::Io(
            io::Error::new(
                io::ErrorKind::Other,
                format!(
                    "unexpected status code {} while loading {}: {}",
                    err.status(),
                    path.display(),
                    err.into_inner(),
                ),
            )
            .into(),
        )
    })?;

    match response.status() {
        StatusCode::Ok => {
            let buf = ContinuousPoll(response.body_bytes())
                .await
                .map_err(|_| AssetReaderError::NotFound(path.to_path_buf()))?;

            if let Some(cache_path) = cache_path {
                if let Some(parent_dirs) = cache_path.parent() {
                    fs::create_dir_all(parent_dirs)?;
                }
                // see https://github.com/johanhelsing/bevy_web_asset/issues/28
                // too many request made to .meta can cause issue
                let mut file = fs::OpenOptions::new()
                    .create(true)
                    .truncate(true)
                    .write(true)
                    .open(&cache_path)?;

                file.write_all(buf.as_slice())?;

                Ok(Box::new(VecReader::new(fs::read(&cache_path)?)))
            } else {
                Ok(Box::new(VecReader::new(
                    ContinuousPoll(response.body_bytes())
                        .await
                        .map_err(|_| AssetReaderError::NotFound(path.to_path_buf()))?,
                )) as _)
            }
        }
        // StatusCode::Ok => Ok(Box::new(VecReader::new(
        //     ContinuousPoll(response.body_bytes())
        //         .await
        //         .map_err(|_| AssetReaderError::NotFound(path.to_path_buf()))?,
        // )) as _),
        StatusCode::NotFound => Err(AssetReaderError::NotFound(path)),
        code => Err(AssetReaderError::Io(
            io::Error::new(
                io::ErrorKind::Other,
                format!(
                    "unexpected status code {} while loading {}",
                    code,
                    path.display()
                ),
            )
            .into(),
        )),
    }
}

use sha2::{Digest, Sha256};

impl AssetReader for WebAssetReader {
    fn read<'a>(
        &'a self,
        path: &'a Path,
    ) -> impl ConditionalSendFuture<Output = Result<Box<Reader<'a>>, AssetReaderError>> {
        let uri = self.connection.make_uri(path);

        let cache_path = self.get_cache_path(&uri);
        get(uri, cache_path)
    }

    async fn read_meta<'a>(&'a self, path: &'a Path) -> Result<Box<Reader<'a>>, AssetReaderError> {


        return Err(AssetReaderError::NotFound(
                "no meta".into(),
            ));

        match self.connection.make_meta_uri(path) {
            Some(uri) => {
                let cache_path = self.get_cache_path(&uri);
                match get(uri, cache_path).await {
                    Ok(reader) => Ok(reader),
                    Err(err) => Err(AssetReaderError::NotFound(
                        format!("Error loading meta: {err}").into(),
                    )),
                }
            }
            None => Err(AssetReaderError::NotFound(
                "source path has no extension".into(),
            )),
        }
    }

    async fn is_directory<'a>(&'a self, _path: &'a Path) -> Result<bool, AssetReaderError> {
        Ok(false)
    }

    async fn read_directory<'a>(
        &'a self,
        path: &'a Path,
    ) -> Result<Box<PathStream>, AssetReaderError> {
        Err(AssetReaderError::NotFound(self.connection.make_uri(path)))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn make_http_uri() {
        assert_eq!(
            WebAssetReaderConnection::Http
                .make_uri(Path::new("s3.johanhelsing.studio/dump/favicon.png"))
                .to_str()
                .unwrap(),
            "http://s3.johanhelsing.studio/dump/favicon.png"
        );
    }

    #[test]
    fn make_https_uri() {
        assert_eq!(
            WebAssetReaderConnection::Https
                .make_uri(Path::new("s3.johanhelsing.studio/dump/favicon.png"))
                .to_str()
                .unwrap(),
            "https://s3.johanhelsing.studio/dump/favicon.png"
        );
    }

    #[test]
    fn make_http_meta_uri() {
        assert_eq!(
            WebAssetReaderConnection::Http
                .make_meta_uri(Path::new("s3.johanhelsing.studio/dump/favicon.png"))
                .expect("cannot create meta uri")
                .to_str()
                .unwrap(),
            "http://s3.johanhelsing.studio/dump/favicon.png.meta"
        );
    }

    #[test]
    fn make_https_meta_uri() {
        assert_eq!(
            WebAssetReaderConnection::Https
                .make_meta_uri(Path::new("s3.johanhelsing.studio/dump/favicon.png"))
                .expect("cannot create meta uri")
                .to_str()
                .unwrap(),
            "https://s3.johanhelsing.studio/dump/favicon.png.meta"
        );
    }

    #[test]
    fn make_https_without_extension_meta_uri() {
        assert_eq!(
            WebAssetReaderConnection::Https
                .make_meta_uri(Path::new("s3.johanhelsing.studio/dump/favicon")),
            None
        );
    }
}
