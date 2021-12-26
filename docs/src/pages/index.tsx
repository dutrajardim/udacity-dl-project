import React from "react"
import { graphql, useStaticQuery } from "gatsby"
import Layout from "../components/layout"

const gql = graphql`
{
    markdownRemark(frontmatter: {title: {eq: "home"}}) {
        html
        tableOfContents
    }
}
`
export default function IndexPage() {
    const result = useStaticQuery(gql)

    return (
        <Layout>
            <div className="row">
                <div 
                    className="col col-md-3 order-md-2 mb-5"
                    dangerouslySetInnerHTML={{ __html: result.markdownRemark.tableOfContents }}></div>
                <div 
                    className="col col-md-9 order-md-1" 
                    dangerouslySetInnerHTML={{ __html: result.markdownRemark.html }}></div>
            </div>
        </Layout>
    )
}