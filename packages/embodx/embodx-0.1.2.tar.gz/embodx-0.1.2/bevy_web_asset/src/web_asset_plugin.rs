use bevy::prelude::*;

use crate::web_asset_source::*;
use bevy::asset::io::AssetSource;

/// Add this plugin to bevy to support loading http and https urls.
///
/// Needs to be added before Bevy's `DefaultPlugins`.
///
/// # Example
///
/// ```no_run
/// # use bevy::prelude::*;
/// # use bevy_web_asset::WebAssetPlugin;
///
/// let mut app = App::new();
///
/// app.add_plugins((
///     WebAssetPlugin::default(),
///     DefaultPlugins
/// ));
/// ```
#[derive(Default)]
pub struct WebAssetPlugin {
    pub cache_resource: bool,
}

impl Plugin for WebAssetPlugin {
    fn build(&self, app: &mut App) {
        let cache_resource = self.cache_resource;
        app.register_asset_source(
            "http",
            AssetSource::build().with_reader(move || {
                Box::new(WebAssetReader {
                    cache_resource,
                    connection: WebAssetReaderConnection::Http,
                })
            }),
        );
        app.register_asset_source(
            "https",
            AssetSource::build().with_reader(move || {
                Box::new(WebAssetReader {
                    cache_resource,
                    connection: WebAssetReaderConnection::Https,
                })
            }),
        );
    }
}
