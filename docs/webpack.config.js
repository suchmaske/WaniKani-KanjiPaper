const webpack = require("webpack");

module.exports = {

    entry: "./src/js/main.js",

    output: {
        filename: "./dist/js/wkkp.bundle.js"
    },

    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            }
        ]
    },

    resolve: {
        alias: {
            vue: 'vue/dist/vue.js'
        }
    }

};

