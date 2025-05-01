const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
  
})

module.exports = {
  lintOnSave: false,
  devServer: {
    port: 3000 // Меняем порт на 3000
  }
}

