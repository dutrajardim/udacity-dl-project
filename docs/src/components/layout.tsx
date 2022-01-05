import React, { useState, useMemo, useRef, useEffect } from 'react'
import { Link } from 'gatsby'
import "../styles/index.scss"

export default function Layout(props: {
    children: JSX.Element[] | JSX.Element
}) {
    const [{ isCollapsed, isCollapsing, collapsingStarted }, setNavState] = useState({
        isCollapsed: false,
        isCollapsing: false,
        collapsingStarted: false
    })
    const [height, setHeight] = useState(0)

    const ref = useRef(null)
    useEffect(() => {
        if (ref && ref.current) setHeight(ref.current.clientHeight)
    }, [ref])

    const collapse = () => {
        setNavState({ isCollapsed, collapsingStarted, isCollapsing: true })

        if (isCollapsed)
            setTimeout(() => setNavState({ isCollapsed: true, isCollapsing: true, collapsingStarted: true }), 10)

        setTimeout(() => setNavState({ isCollapsed: !isCollapsed, isCollapsing: false, collapsingStarted: false }), 300)
    }

    let navStyles = useMemo(() =>
        (collapsingStarted && isCollapsed) ? { height } : {}, [collapsingStarted, isCollapsed, height])

    let classes = useMemo(() => {
        return `navbar-collapse ${isCollapsing ? 'collapsing' : 'collapse'} ${isCollapsed || isCollapsing ? '' : 'show'}`
    }, [isCollapsing, isCollapsed])

    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                <div className="container">
                    <Link className="navbar-brand" to="/">Dutra Jardim</Link>
                    <button className="navbar-toggler" type="button" onClick={collapse}>
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className={classes} style={navStyles} ref={ref}>
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <li className="nav-item">
                                <Link className="nav-link" to="/">Home</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/files">Docstrings</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/charts">Charts</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            <div className='pb-5 pt-5 bg-light'>
                <main className="container">
                    {props.children}
                </main>
            </div>
            <div className='pt-4 bg-dark'>
                <footer className='container'>
                    <div className="row">
                        <div className="col text-center">
                            <img className="img-thumbnail" style={{ width: 120, height: 120, borderRadius: '50%' }} src="https://avatars.githubusercontent.com/u/38335241?s=400&u=cfaa3e23df4fa874144dcb250b972752bb492ab1&v=4" />
                            <p className='text-light flat-right mt-4'>
                                <a className="me-4" href='www.linkedin.com/in/rafael-dutra-jardim' target="_blank">
                                    <i className="bi bi-linkedin text-light" style={{ fontSize: '2rem' }}></i>
                                </a>
                                <a href='https://github.com/dutrajardim/udacity-dl-project' target="_blank">
                                    <i className="bi bi-github text-light" style={{ fontSize: '2rem' }}></i>
                                </a>
                            </p>
                        </div>
                    </div>
                </footer>
            </div>
        </>
    )
}