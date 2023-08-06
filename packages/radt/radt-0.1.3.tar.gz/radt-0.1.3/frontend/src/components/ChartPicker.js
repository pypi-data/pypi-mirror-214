import React from 'react';
import { HTTP } from '../api';
import Chart from './Chart';
import '../styles/ChartPicker.css';
import DataIcon from '../images/data.svg';
import UploadIcon from '../images/upload.svg';
import DownloadIcon from '../images/download.svg';
import LoadingIcon from '../images/cogwheel.svg';

class ChartPicker extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			loading: false,
			availableMetrics: [],
			showMetrics: false,
			charts: []
		};

		this.inputField = React.createRef();
	}

	componentDidMount() {
		// fetch available metrics for any selected runs
		this.fetchMetrics(this.props.pushSelectedRuns);

		// check localSStorage for pre-existing chart data
		const localCharts = JSON.parse(localStorage.getItem("localCharts"))
		if (localCharts !== null && localCharts.length !== 0) {
			this.setCharts(localCharts);
			this.props.toggleDataPicker(false);
			console.log("GET: charts loaded from localStorage");
		}
	}

	componentDidUpdate(prevProps) {
		const toHide =  this.props.toHide;
		if (prevProps.toHide !== toHide) {
			const selectedRuns = this.props.pushSelectedRuns;
			this.fetchMetrics(selectedRuns);
		}
	}

	// fetch all available metrics for the current selected runs 
	async fetchMetrics() {
		const selectedRuns = this.props.pushSelectedRuns;	
		const data = await HTTP.fetchMetrics(selectedRuns);
		this.setState({availableMetrics: data});
	}

	// toggle metric list visibility 
	toggleMetrics() {
		const toShow = this.state.showMetrics;
		this.setState({ showMetrics: !toShow})
	}

	// fetch all data for each run 
	async fetchChartData(metric) {

		this.setState({ 
			loading: true,
			showMetrics: false
		});

		// deep clone run selections and fetch chart data for each run
		const chartRuns = structuredClone(this.props.pushSelectedRuns);
		let chartData = await HTTP.fetchChart(chartRuns, metric);

		// prevent app getting stuck on load if server fails to fetch
		if (chartData.length === 0) {
			this.setState({ loading: false });
			return;
		}

		// add the run data to the cloned run selections
		chartData.forEach(data => {	
			chartRuns.forEach(run => {
				if (run.name === data.name) {			
					if (run.data === undefined) {
						run.data = [];
					}
					run.data.push({
						timestamp: data.timestamp,
						value: data.value,
						step: data.step,
					});
				}
			});
		});

		// add the new chart data to the state with a unique ID based on unix timestamp
		let newCharts = [...this.state.charts];
		const chartId = Date.now();
		newCharts.push({ 
			id: chartId,
			data: chartRuns,
			metric: metric,
			context: {
				smoothing: 0,
				shownRuns: [],
				hiddenSeries: [],
				range: {min: 0, max: 0}
			}
		});

		// update chart state with new data
		this.setCharts(newCharts);
	}

	// removes chart from state using its id 
	removeChart(id) {
		let newCharts = [...this.state.charts].filter(chart => chart.id !== id);
		this.setCharts(newCharts);
	}

	// add chart data to state for rendering 
	setCharts(newChartData) {

		// apply chart data to state
		this.setState({
			charts: newChartData,
			loading: false,
		});

		// open data picker if no charts loaded
		if (newChartData.length === 0) {
			localStorage.removeItem("localCharts");
			//this.props.toggleDataPicker(true);	
		}
		else {
			// toggle data picker off if on
			this.props.toggleDataPicker(false);	

			// save data to local storage to persist through refreshes
			//storeChartDataInLocalStorage(newChartData);
		}
	}

	// update custom chart state for local data download
	syncData(id, newSmoothing, newShownRuns, newHiddenSeries, newRange) {
		const chartData = [...this.state.charts];
		chartData.forEach(chart => {
			if (chart.id === id) {
				chart.context.smoothing = newSmoothing;
				chart.context.shownRuns = newShownRuns;
				chart.context.hiddenSeries = newHiddenSeries;		
				chart.context.range = newRange;
			}
		})
		this.setState({
			charts: chartData,
		});
	}

	// upload data from a locally saved .json file
	async uploadLocalData() {

		const uploadedData = await new Promise((resolve) => {
			if (window.File && window.FileReader && window.FileList && window.Blob) {
				var file = document.querySelector('input[type=file]').files[0];
				var reader = new FileReader()
				var textFile = /json.*/;
				if (file.type.match(textFile)) {
					reader.onload = function (event) {
						try {
							const data = JSON.parse(event.target.result);
							//console.log(data); // debugging
							resolve(data);
						}
						catch {
							alert("Incompatible data file!");
						}			
					}
				} 
				else {
				   alert("Incompatible data file!");
				}
				reader.readAsText(file);
			} 
			else {
				alert("This browser is too old to support uploading data.");
			}
		});

		// clear file from hidden upload input
		this.inputField.current.value = "";
		
		const reversedUploadedData = uploadedData.reverse();

		// update with new id's so they are unique 
		for (let i = 0; i < reversedUploadedData.length; i++) {
			const chart = reversedUploadedData[i];
			chart.id = Date.now() + i;
		}
		const newChartData = [...this.state.charts, ...reversedUploadedData];

		// set uploaded data as new charts
		this.setCharts(newChartData);
	}

	// download data to a locally saved .json file
	downloadLocalData() {
		if (this.state.charts.length > 0) {
			const chartDataString = JSON.stringify(this.state.charts);
			const fileName = "data_" + new Date().toISOString() + ".json";
			const blob = new Blob([chartDataString], {type: 'text/plain'});
			if(window.navigator.msSaveOrOpenBlob) {
				window.navigator.msSaveBlob(blob, fileName);
			}
			else{
				const elem = window.document.createElement('a');
				elem.href = window.URL.createObjectURL(blob);
				elem.download = fileName;        
				document.body.appendChild(elem);
				elem.click();        
				document.body.removeChild(elem);
			}
			console.log("Downloading data... " + fileName);
		}
		else {
			alert("No chart data to download.")
		}	
	}

	render() {
		const { availableMetrics, showMetrics, charts, loading } = this.state;
		return (
			<div id="chartPickerWrapper">

				{/*} Data Button {*/}
				<button 
					id="dataLogo"
					onClick={() => this.props.toggleDataPicker(true)}
					className={this.props.toHide ? null : "hide"}
				>
					<img src={DataIcon} className="dataSVG" alt="Choose Data" title="Choose Data" />
				</button>

				{/*} Download & Upload Buttons {*/}
				<div 
					id="downloadUploadWrapper"
					//className={this.props.toHide ? null : "hide"}
				>			
					<label className="upload" htmlFor="hiddenUpload">
						<input id="hiddenUpload" type="file" ref={this.inputField} onChange={this.uploadLocalData.bind(this)} />
						<img src={UploadIcon} className="uploadSVG" alt="Upload Charts" title="Upload Charts" />
					</label>
					
					<button className="download" onClick={() => this.downloadLocalData()}>
						<img src={DownloadIcon} className="downloadSVG" alt="Download Charts" title="Download Charts" />
					</button>
				</div>

				{/*} Pick Chart Button {*/}
				<button 
					id="pickChartBtn"
					onClick={() => this.toggleMetrics()}
					disabled={loading ? true : ""}
					title="Choose Metric"
					//className={availableMetrics.length === 0 ? "hide" : null}
				>
					{loading ? <img src={LoadingIcon} className="loadingIcon" alt="Loading..." /> : "+"}
				</button>

				{/*} Metrics List {*/}
				<div 
					id="metricBtnList"
					className={showMetrics ? null : "hide"}
				>
					{availableMetrics.map(metric => (
						<button
							key={metric}
							className="metricBtn"
							onClick={() => this.fetchChartData(metric)}
						>
							{metric}
						</button>
					))}
					<div id="noData" className={availableMetrics.length === 0 ? null : "hide"}>No data available for current selection.</div>
				</div>

				{/*} Charts List {*/}
				<div id="chartsWrapper">
					{charts.sort((a, b) => b.id - a.id).map(chart => (
						<Chart 
							key={chart.id} 
							chartData={chart}
							pullChartExtras={this.syncData.bind(this)}
							removeChart={this.removeChart.bind(this)}
						/>
					))}
				</div>		
			</div>
		);
	}
}


/* ChartPicker helper functions */
/*
function storeChartDataInLocalStorage(chartData) {
	let chartDataToBeLoaded = chartData.sort((a, b) => b.id - a.id);
	for (let i = 1; i < chartData.length + 1; i++) {	
		try {
			const newChartsString = JSON.stringify(chartDataToBeLoaded);
			localStorage.setItem("localCharts", newChartsString);
			break;
		}
		catch {

			chartDataToBeLoaded = chartData.slice(0, i * -1);
			continue;
		}
	}
}
*/
export default ChartPicker;