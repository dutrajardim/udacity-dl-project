import * as React from "react"

import Layout from "../components/layout"
import PlaysByLevelWeekdayBar from "../charts/PlaysByLevelWeekdayBar"
import PlaysByLevelPie from "../charts/PlaysByLevelPie"
import PlaysByGenderPie from "../charts/PlaysByGenderPie"
import PlaysByGenderWeekScatter from "../charts/PlaysByGenderWeekScatter"
import ArtistsFiveMostListenedTable from "../charts/ArtistsFiveMostListenedTable"

const IndexPage = () => {
	return (
		<Layout>
			<div className="row">
				<div className="col">
					<div className="card mt-2">
						<div className="card-body">
							<PlaysByLevelPie />
						</div>
					</div>
				</div>
			</div>
			<div className="row">
				<div className="col">
					<div className="card mt-2">
						<div className="card-body">
							<PlaysByLevelWeekdayBar />
						</div>
					</div>
				</div>
			</div>
			<div className="row">
				<div className="col">
					<div className="card mt-2">
						<div className="card-body">
							<ArtistsFiveMostListenedTable />
						</div>
					</div>
				</div>
			</div>
			<div className="row">
				<div className="col">
					<div className="card mt-2">
						<div className="card-body">
							<PlaysByGenderPie />
						</div>
					</div>
				</div>
			</div>
			<div className="row">
				<div className="col">
					<div className="card mt-2">
						<div className="card-body">
							<PlaysByGenderWeekScatter />
						</div>
					</div>
				</div>
			</div>
		</Layout>
	)
}

export default IndexPage
