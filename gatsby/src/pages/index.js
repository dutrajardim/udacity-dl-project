import * as React from "react"

import Layout from "../components/layout"
import LevelCountingByWeekdayChart from "../charts/LevelCountingByWeekdayChart"
import CountingByLevelChart from "../charts/CountingByLevelChart"
import ArtistsFiveMostListenedTable from "../charts/ArtistsFiveMostListenedTable"

const IndexPage = () => {
	return (
		<Layout>
			<div className="row">
				<div className="col">
					<div className="card mt-2">
						<div className="card-body">
							<CountingByLevelChart />
						</div>
					</div>
				</div>
			</div>
			<div className="row">
				<div className="col">
					<div className="card mt-2">
						<div className="card-body">
							<LevelCountingByWeekdayChart />
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
		</Layout>
	)
}

export default IndexPage
