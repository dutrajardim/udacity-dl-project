import React from 'react'
import { useStaticQuery, graphql } from 'gatsby'
import Plot from 'react-plotly.js'

const gql = graphql`
    query {
        data: allOlapYaerWeekGender(
            filter: {week: {eq: null}, year: {eq: null}, gender: {ne: null}}
        ) {
            edges {
                node {
                    count
                    gender
                }
            }
        }
    }
`

const labelsMap = {
    'F': 'Female',
    'M': 'Male',
    'unknown': 'Anonymous'
}

export default function PlaysByGenderPie() {
    const resp = useStaticQuery(gql)
    const reducer = (acc, { node }) => ([[...acc[0], node.gender], [...acc[1], node.count]])
    const [labels, values] = resp.data.edges.reduce(reducer, [[], []])

    const countingTrace = {
        type: 'pie',
        values: values,
        labels: labels.map(v => labelsMap[v])
    }

    return (
        <Plot
            data={[countingTrace]}
            layout={{ title: 'Counting by gender' }} />
    )
}