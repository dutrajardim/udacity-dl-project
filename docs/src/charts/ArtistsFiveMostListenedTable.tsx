// import React from 'react'
// import { useStaticQuery, graphql } from 'gatsby'

// const gql = graphql`
//     query {
//         fiveMostListened: allOlapLevelWeekdayArtists(
//             sort: {fields: count, order: DESC}
//             filter: {level: {eq: null}, weekday: {eq: null}, name: {nin: [null, "unknown"]}}
//             limit: 5
//         ) {
//             edges {
//                 node {
//                     count
//                     name
//                 }
//             }
//         }
//     }
// `

// export default function ArtistsFiveMostListenedTable() {
//     const resp = useStaticQuery(gql)
//     const fiveMost = resp.fiveMostListened.edges.map(({ node }) => node)

//     return (
//         <div className="table-responsive" style={{ maxHeight: '200px' }}>
//             <table className="table table-sm">
//                 <thead>
//                     <tr>
//                         <th className="col">#</th>
//                         <th className="col">Artist</th>
//                         <th className="col">Count</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//                     {fiveMost.map(({ name, count }, idx) => (
//                         <tr key={idx}>
//                             <th scope="row">{idx + 1}</th>
//                             <td>{name}</td>
//                             <td>{count}</td>
//                         </tr>
//                     ))}
//                 </tbody>
//             </table>
//         </div>
//     )
// }