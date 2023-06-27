// Based on https://github.com/rclrust/rclrust/tree/3a48dbb8f23a3d67d3031351da3ed236a354f039/rclrust-msg-gen

#![warn(
    rust_2018_idioms,
    elided_lifetimes_in_paths,
    clippy::all,
    clippy::nursery
)]

mod parser;
mod types;

use std::path::Path;

use proc_macro::TokenStream;
use quote::quote;

use crate::parser::get_packages;

#[proc_macro]
pub fn msg_include_all(_input: TokenStream) -> TokenStream {
    let ament_prefix_path = std::env!("DETECTED_AMENT_PREFIX_PATH");
    let paths = ament_prefix_path
        .split(':')
        .map(Path::new)
        .collect::<Vec<_>>();

    let packages = get_packages(&paths)
        .unwrap()
        .iter()
        .map(|v| v.token_stream())
        .collect::<Vec<_>>();

    (quote! {
        #(#packages)*
    })
    .into()
}
