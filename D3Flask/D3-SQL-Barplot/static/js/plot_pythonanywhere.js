// The base endpoint to receive data from. See function "update_url"
var URL_BASE = "http://ankoorb.pythonanywhere.com/query/" // Change this when you need to deploy


// Update plot in response to a users inputs
// Select id's of <select> tag for different dropdown menus and update plot based on input
d3.select("#borough_select").on("input", plot_figure);
d3.select("#time_slide").on("input", plot_figure);

var margin = {top: 20, right: 20, bottom: 20, left: 60};
var width = 800 - margin.left - margin.right;
var height = 400 - margin.top - margin.bottom;

// Scale: Padding = 0.1
var x = d3.scale.ordinal()
			.rangeRoundBands([0, width], 0.1); 
			
var y = d3.scale.linear()
			.range([height, 0]);
			
// Axis
var xAxis = d3.svg.axis()
			.scale(x)
			.orient("bottom");
						
var yAxis = d3.svg.axis()
			.scale(y)
			.orient("left")
			.ticks(10);
			
var svg = d3.select("body").append("svg")
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
						
// X Axis
svg.append("g")
	.attr("class", "x axis")
	.attr("transform", "translate(0," + height + ")")
	.call(xAxis)
	.append("text")
	.text("Agency")
	.attr("dy", "3em")
	.attr("text-align", "right")
	.attr("x", width / 2 - margin.right - margin.left);
				
// Y Axis
svg.append("g")
	.attr("class", "y axis")
	.call(yAxis)
	.append("text")
	.attr("transform", "rotate(-90)")
	.text("Count")
	.attr('y', 6)
	.attr("dy", "0.7em")
	.style('text-anchor', 'end')
		
// Function to update the time displayed (xx:xx) next to the time slider
function update_slider(time){
	// Create a new date object and set hours and minutes
	var dateObj = new Date()
	dateObj.setHours(Math.floor(time/60))
	dateObj.setMinutes(time % 60)
	// Select id of <span> tag for time slider
	d3.select("#pretty_time")
		.text(dateObj.toTimeString().substring(0, 5)) // Convert date object to time string and update text with substring
	}
	
// When a user selects an option a function is called to update url to recieve data in csv format with query filled in the form of input fields from SQL database
function update_url(){
	// document.getElementById("id"): Get the element with the specified "id" (from index.html)
	
	// URL: http://localhost:5000/?borough=Manhattan&minute=600
	return URL_BASE + 
			"?borough=" + document.getElementById("borough_select").value +
			"&minute=" + document.getElementById("time_slide").value;
}

// Function to convert string data to number data
function type(d){
	d['count'] = +d['count'];
	return d
}

// Function to plot figure
function plot_figure(){
	// Update time slider
	update_slider(+document.getElementById("time_slide").value);
	
	// Get data 
	url = update_url()
	
	
	d3.csv(url, type, function(error, data){
		
		//console.log(data);
		
		// Domain of X scale
		x.domain(data.map(function(d){return d["agency"]}));
		
		svg.selectAll("g.x.axis")
			.call(xAxis);
		
		// Domain of Y scale
		y.domain([0, d3.max(data, function(d){return d["count"]})]);
		
		svg.selectAll("g.y.axis")
			.call(yAxis);
		
		var bars = svg.selectAll(".bar")
			.data(data);
			//.data(data, function(d){return d["agency"]});
					
		bars.transition(1000)
			.attr('x', function(d){return x(d['agency'])})
			.attr('width', x.rangeBand())
			.attr("y", function(d){return y(d['count'])})
			.attr("height", function(d){return height - y(d['count'])})
			
		bars.enter().append("rect")
			.attr("class", "bar")
			.attr("x", function(d){return x(d["agency"])})
		.attr('width', x.rangeBand())
			.attr("y", height)
			.attr("height", 0)
			.transition(1000)
			.attr("y", function(d){return y(d['count'])})
			.attr("height", function(d){return height - y(d['count'])});

		bars.exit()
			.transition(1000)
			.attr("y", height)
			.attr("height", 0)
			.remove();
			
	});
	
}

// Call the plotting function
plot_figure()



