import React from "react"

import Layout from "../components/layout"
import PlaysByLevelWeekdayBar from "../charts/PlaysByLevelWeekdayBar"
import PlaysByLevelPie from "../charts/PlaysByLevelPie"
import PlaysByGenderPie from "../charts/PlaysByGenderPie"
import PlaysByGenderWeekScatter from "../charts/PlaysByGenderWeekScatter"
import ArtistsFiveMostListenedTable from "../charts/ArtistsFiveMostListenedTable"

export default function ChartsPage() {
	return (
		<Layout>
			<div className="row">
				<div className="col">
					<h2>Charts example</h2>
					<p>
						As the result of the queries are stored in an S3 bucket, on each build of the
						Gatsby Js, a script using the Minio Js framework downloads the parquet files, that are read with
						the help of the <a href="https://github.com/ZJONSSON/parquetjs" target="_blank">parquetjs-lite</a> package,
						and then rendered the charts by <a href="https://plotly.com/javascript/" target="_blank">Plotly.js</a>.
					</p>
				</div>
			</div>
			<div className="row row-cols-1 row-cols-md-3 g-4 mt-3">
				<div className="col">
					<div className="card shadow rounded">
						<div className="card-body">
							<div className="card-title">Counting plays by level</div>
							<PlaysByLevelPie />
						</div>
					</div>
				</div>
				<div className="col">
					<div className="card shadow rounded">
						<div className="card-body">
							<div className="card-title">Counting plays by gender</div>
							<PlaysByGenderPie />
						</div>
					</div>
				</div>
				<div className="col">
					<div className="card shadow rounded h-100">
						<div className="card-body">
							<div className="card-title">Five artists most listened</div>
							<ArtistsFiveMostListenedTable />
						</div>
					</div>
				</div>
			</div>
			<div className="row row-cols-1 row-cols-md-2 g-4 mt-3">
				<div className="col">
					<div className="card shadow rounded">
						<div className="card-body">
							<div className="card-title">Counting plays by level in week days</div>
							<PlaysByLevelWeekdayBar />
						</div>
					</div>
				</div>
				<div className="col">
					<div className="card shadow rounded">
						<div className="card-body">
							<div className="card-title">Counting plays by gender in week</div>
							<PlaysByGenderWeekScatter />
						</div>
					</div>
				</div>
			</div>
		</Layout>
	)
}
