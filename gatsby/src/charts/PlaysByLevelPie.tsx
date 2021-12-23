// import React from 'react'
// import { useStaticQuery, graphql } from "gatsby"
// import Plot from "react-plotly.js"

// import { capitalizeFirstLetter } from "../helpers"

// const gql = graphql`
//     query LevelWeekdayArtistCube {
//         data: allOlapLevelWeekdayArtists(
//             filter: {name: {eq: null}, weekday: {eq: null}, level: {ne: null}}
//         ) {
//             edges {
//                 node {
//                     level
//                     count
//                 }
//             }
//         }
//     }
// `

// export default function PlaysByLevelPie() {
//     const resp = useStaticQuery(gql)
//     const reducer = (acc, { node }) => ([[...acc[0], node.level], [...acc[1], node.count]])
//     const [labels, values] = resp.data.edges.reduce(reducer, [[], []])

//     const levelTrace = {
//         type: 'pie',
//         values,
//         labels: labels.map(capitalizeFirstLetter)
//     }

//     let layout = {
//         autosize: true,
//         margin: { t: 30, b: 0, r: 10, l: 10 },
//         legend: { orientation: "h" }
//     }

//     return (
//         <Plot
//             data={[levelTrace]}
//             layout={layout}
//             useResizeHandler={true}
//             style={{ width: '100%', height: '100%', maxHeight: '200px' }} />
//     )
// }