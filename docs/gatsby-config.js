module.exports = {
  siteMetadata: {
    siteUrl: "https://www.yourdomain.tld",
    title: "Sparkify Data Lake Dashboard",
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
          "**/\__*",
          "**/aws",
          "**/gatsby",
          "**/k8s",
          "**/notebooks",
          "**/setup.py",
          "**/setup.py",
          "**/\.*"
        ]
      }
    },
    "gatsby-transformer-python-docstring"
  ],
};
