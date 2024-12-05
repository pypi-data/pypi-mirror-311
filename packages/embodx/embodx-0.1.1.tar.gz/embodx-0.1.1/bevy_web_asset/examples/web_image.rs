use core::panic;
use std::io;

use bevy::{asset::AssetLoader, prelude::*};
use bevy_web_asset::WebAssetPlugin;
use bevy::{
    asset::{io::Reader, AsyncReadExt, LoadContext},
};

fn main() {
    App::new()
        .add_plugins((
            // The web asset plugin must be inserted before the `AssetPlugin` so
            // that the AssetPlugin recognizes the new sources.
            WebAssetPlugin { cache_resource: true },
            // WebAssetPlugin::default(),
            DefaultPlugins,
        ))
        .add_systems(Startup, setup)
        .init_asset::<UrdfAsset>()
            .init_asset_loader::<UrdfAssetLoader>()
            .init_asset_loader::<FakeImageAssetLoader>()
        .run();
}


#[derive(Asset, TypePath, Debug)]
pub(crate) struct UrdfAsset {
}

#[derive(Default)]
struct UrdfAssetLoader;

#[derive(Default)]
struct FakeImageAssetLoader;

impl AssetLoader for UrdfAssetLoader {
    type Asset = UrdfAsset;
    type Settings = ();
    type Error = io::Error;

    async fn load<'a>(
        &'a self,
        reader: &'a mut Reader<'_>,
        _settings: &'a (),
        load_context: &'a mut LoadContext<'_>,
    ) -> Result<Self::Asset, Self::Error> {
        panic!("Not implemented");
    }

    fn extensions(&self) -> &[&str] {
        &["urdf", "stl"]
    }
}

impl AssetLoader for FakeImageAssetLoader {
    type Asset = Image;
    type Settings = ();
    type Error = io::Error;

    async fn load<'a>(
        &'a self,
        reader: &'a mut Reader<'_>,
        _settings: &'a (),
        load_context: &'a mut LoadContext<'_>,
    ) -> Result<Self::Asset, Self::Error> {
        let mut bytes = Vec::new();
        reader.read_to_end(&mut bytes).await?;

        let a = load_context.read_asset_bytes("https://raw.githubusercontent.com/Daniella1/urdf_files_dataset/refs/heads/main/urdf_files/random/robot-assets/franka_panda/meshes/collision/link0.stl").await.unwrap();

        // dbg!(a);

        // std::str::from_utf8(&bytes).unwrap();

        // if let Some(urdf_robot) = std::str::from_utf8(&bytes)
        //     .ok()
        //     .and_then(|utf| Some(utf))
        // {
        //     dbg!("loaded", urdf_robot);
        //     let base_dir = load_context.asset_path().parent();
        // } else {
        //     dbg!("failed to load");
        // }
        // // Ok(Image {})

        panic!("Not implemented");

    }

    fn extensions(&self) -> &[&str] {
        &["urdf", "stl"]
    }
}


fn setup(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn(Camera2dBundle::default());

    commands.spawn(SpriteBundle {
        // Simply use a url where you would normally use an asset folder relative path
        // texture: asset_server.load("https://raw.githubusercontent.com/Daniella1/urdf_files_dataset/refs/heads/main/urdf_files/random/robot-assets/franka_panda/panda.urdf"),
        texture: asset_server.load("https://s3.johanhelsing.studio/dump/favicon.png"),
        // texture:asset_server.load("https://raw.githubusercontent.com/Daniella1/urdf_files_dataset/refs/heads/main/urdf_files/random/robot-assets/franka_panda/meshes/collision/link0.stl"),
        ..default()
    });

    // let a: Handle<Image> = asset_server.load("https://s3.johanhelsing.studio/dump/favicon.png");

    // let a: Handle<UrdfAsset> = asset_server.load("https://raw.githubusercontent.com/Daniella1/urdf_files_dataset/refs/heads/main/urdf_files/random/robot-assets/franka_panda/panda.urdf");
    // let a: Handle<UrdfAsset> = asset_server.load("https://raw.githubusercontent.com/Daniella1/urdf_files_dataset/refs/heads/main/urdf_files/random/robot-assets/franka_panda/meshes/collision/link0.stl");


    // let a: Handle<Image> = asset_server.load("https://raw.githubusercontent.com/openrr/urdf-viz/refs/heads/main/sample.urdf");
}
