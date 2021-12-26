import React from 'react'
import Layout from '../components/layout'
import FilesNav from '../components/filesNav'

export default function PythonFiles () {
    return (
        <Layout>
            <div className="row">
                <div className="col col-md-3 order-md-2 mb-5">
                    <FilesNav />
                </div>
                <div className="col col-md-9 order-md-1">
                    
                </div>
            </div>
        </Layout>
    )
}