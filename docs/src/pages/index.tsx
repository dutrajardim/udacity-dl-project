import React from "react"
import { graphql, useStaticQuery } from "gatsby"
import Layout from "../components/layout"

const gql = graphql`
{
    markdownRemark(frontmatter: {title: {eq: "home"}}) {
        html
    }
}
`
export default function IndexPage() {
    const result = useStaticQuery(gql)

    return (
        <Layout>
            <div className="row">
                <div
                    className="col"
                    dangerouslySetInnerHTML={{ __html: result.markdownRemark.html }}></div>
            </div>
        </Layout>
    )
}