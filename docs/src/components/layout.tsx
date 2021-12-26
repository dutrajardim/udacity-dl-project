import React from 'react'
import { Link } from 'gatsby'
import "../styles/index.scss"

export default function Layout(props: {
    children: JSX.Element[] | JSX.Element
}) {
    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-light">
                <div className="container">
                    <Link className="navbar-brand" to="/">DL - Udacity Project</Link>
                    <button className="navbar-toggler" type="button">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <li className="nav-item">
                                <Link className="nav-link" to="/">Home</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/files">Docstrings</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            <div className='pb-5 pt-5 bg-light'>
                <main className="container">{props.children}</main>
            </div>
        </>
    )
}