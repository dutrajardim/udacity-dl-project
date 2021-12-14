import React from 'react'

import "../styles/index.scss"

export default function Layout(props: {
    children: JSX.Element[] | JSX.Element
}) {
    return (
        <div className='mb-5 bg-light'>
            <header></header>
            <main className="container">{props.children}</main>
        </div>
    )
}