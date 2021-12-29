module.exports = {
  siteMetadata: {
    siteUrl: "https://www.yourdomain.tld",
    title: "Sparkify Data Lake Dashboard",
    githubProjectUrl: "https://github.com/dutrajardim/udacity-dl-project/blob/main"
  },
  plugins: [
    "gatsby-plugin-sass",
    "gatsby-plugin-react-helmet",
    // "gatsby-source-olap"
    {
      resolve: "gatsby-source-filesystem",
      options: {
        name: 'python-files',
        path: `${__dirname}/..`,
        ignore: [
          "**/\_\_*",
          "**/aws",
          "**/docs",
          "**/k8s",
          "**/notebooks",
          "**/\.*",
          "**/requirements*",
          "**/build",
          "**/dist",
          "**/sparkify_etls.egg-info"
        ]
      }
    },
    require.resolve('./plugins/gatsby-transformer-python-docstring/dist'),
    "gatsby-transformer-remark"
  ],
};
