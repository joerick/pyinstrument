module.exports = {
  configureWebpack: {
    optimization: {
      splitChunks: false
    },
  },
  filenameHashing: false,
  css: {
     extract: false,
  },
  chainWebpack: config => {
      config.module
            .rule('images')
            .use('url-loader')
                .loader('url-loader')
                .tap(options => {
                    // inline everything
                    options.limit = undefined;
                    return options
                })
      config.module
            .rule('svg')
            .use('url-loader')
                .loader('url-loader')
                .tap(options => {
                    options = options || {}
                    // inline everything
                    options.limit = undefined;
                    return options
                })
  }
}
