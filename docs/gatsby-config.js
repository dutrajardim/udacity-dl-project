const process = require('process')
require('dotenv').config({
  path: `.env.${process.env.NODE_ENV}`
})


module.exports = {
  siteMetadata: {
    siteUrl: "https://www.yourdomain.tld",
    title: "Sparkify Data Lake Dashboard",
    githubProjectUrl: "https://github.com/dutrajardim/udacity-dl-project/blob/main"
  },
  plugins: [
    "gatsby-plugin-sass",
    "gatsby-plugin-react-helmet",
    {
      resolve: require.resolve("./plugins/gatsby-source-olap"),
      options: {
        s3: {
          key: process.env.NODE_S3_KEY,
          secret: process.env.NODE_S3_SECRET,
          endpoint: process.env.NODE_S3_ENDPOINT,
        },
        bucket: 'dutrajardim',
        olapCubes: [
          { name: 'LevelWeekdayName', s3Key: 'udacity-dl-project/olap-cubes/users_level-times_weekday-artist_name.parquet' },
          { name: 'YaerWeekGender', s3Key: 'udacity-dl-project/olap-cubes/songs_year-times_week-users_gender.parquet' }
        ]
      }
    },
    {
      resolve: "gatsby-source-filesystem",
      options: {
        name: 'python-files',
        path: `${__dirname}/..`,
        ignore: [
          "**/\_\_*",
          "**/shell_scripts",
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
