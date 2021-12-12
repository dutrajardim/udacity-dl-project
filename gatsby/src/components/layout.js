import React from 'react'

import "../styles/index.scss"

export default function Layout(props) {
    return (
        <div>
            <header></header>
            <main className="container">{props.children}</main>
        </div>
    )
}