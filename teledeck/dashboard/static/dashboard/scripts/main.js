function getFilteredData() {
    //Retrieve messages filtered metrics
    const request = '/dashboard/get-data';
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    const data = xmlHttp.responseText;
    return data;
}

function toggleAllPanels() {
    //Show all panels from "Vue générale"
    const targetElements = document.getElementById('main').children;
    for (let i = 1; i < targetElements.length; i++) {
        if (targetElements[i].attributes.class.value == "d-none b-example-divider b-example-vr") {
            targetElements[i].setAttribute("class", "d-block b-example-divider b-example-vr");
        } else if (targetElements[i].attributes.class.value == "d-none flex-column flex-shrink-0 p-3 bg-light") {
            targetElements[i].setAttribute("class", "d-flex flex-column flex-shrink-0 p-3 bg-light");
        } else if (targetElements[i].attributes.class.value == "d-none flex-column align-items-stretch flex-shrink-0 bg-white p-3") {
            targetElements[i].setAttribute("class", "d-flex flex-column align-items-stretch flex-shrink-0 bg-white p-3");
        }
    }
}

function collapse(id) {
    //Toggle panels from nav bar depending on selected id
    const targetElement = document.getElementById(id);
    const separator = targetElement.nextElementSibling;
    if (targetElement.attributes.class.value == "d-flex flex-column flex-shrink-0 p-3 bg-light resizable") {
        separator.setAttribute("class", "d-none b-example-divider b-example-vr");
        targetElement.setAttribute("class", "d-none flex-column flex-shrink-0 p-3 bg-light resizable");
    } else if (targetElement.attributes.class.value == "d-flex flex-column align-items-stretch flex-shrink-0 bg-white p-3 resizable") {
        separator.setAttribute("class", "d-none b-example-divider b-example-vr");
        targetElement.setAttribute("class", "d-none flex-column align-items-stretch flex-shrink-0 bg-white p-3 resizable");
    } else if (targetElement.attributes.class.value == "d-none flex-column flex-shrink-0 p-3 bg-light resizable") {
        separator.setAttribute("class", "d-block b-example-divider b-example-vr");
        targetElement.setAttribute("class", "d-flex flex-column flex-shrink-0 p-3 bg-light resizable");
    } else if (targetElement.attributes.class.value == "d-none flex-column align-items-stretch flex-shrink-0 bg-white p-3 resizable") {
        separator.setAttribute("class", "d-block b-example-divider b-example-vr");
        targetElement.setAttribute("class", "d-flex flex-column align-items-stretch flex-shrink-0 bg-white p-3 resizable");
    }
}

function updateData() {
    //Request channel group toggle to Django dashboard/views
    const messageThread = document.getElementById('messages');
    const request = '/dashboard/update-data';
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, true);
    xmlHttp.send( null );
    messageThread.innerHTML = xmlHttp.responseText;
    document.getElementById('sort-by-date').addEventListener('click', function() { sortByDate(); });
    document.querySelectorAll('#message-container').forEach(message => { message.addEventListener('click', showDetail); });
}

function toggleChannelGroup(e) {
    const group = e.target.id;
    const sourceDetail = document.getElementById('source-list');
    const request = `/dashboard/toggle-group/${group}`;
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    sourceDetail.innerHTML = xmlHttp.responseText;
    document.querySelectorAll('.form-check-input').forEach(toggle => { toggle.addEventListener('click', toggleChannelGroup); });
    document.querySelectorAll('#channel').forEach(channel => { channel.addEventListener('click', toggleChannel); });
    document.querySelectorAll('#delete-channel').forEach(channel => { channel.addEventListener('click', deleteChannel); });
    updateMessages()
    computeGraph()
}

function toggleChannel(e) {
    //Request channel toggle to Django dashboard/views
    const channel = e.target.innerText;
    const sourceDetail = document.getElementById('source-list');
    const request = `/dashboard/toggle-channel/${channel}`;
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    sourceDetail.innerHTML = xmlHttp.responseText;
    document.querySelectorAll('.form-check-input').forEach(toggle => { toggle.addEventListener('click', toggleChannelGroup); });
    document.querySelectorAll('#channel').forEach(channel => { channel.addEventListener('click', toggleChannel); });
    document.querySelectorAll('#delete-channel').forEach(channel => { channel.addEventListener('click', deleteChannel); });
    updateMessages()
    computeGraph()
}

function deleteChannel(e) {
    const channel = e.target.attributes.value.nodeValue;
    const sourceDetail = document.getElementById('source-list');
    const request = `/dashboard/delete-channel/${channel}`;
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    sourceDetail.innerHTML = xmlHttp.responseText;
    document.querySelectorAll('.form-check-input').forEach(toggle => { toggle.addEventListener('click', toggleChannelGroup); });
    document.querySelectorAll('#channel').forEach(channel => { channel.addEventListener('click', toggleChannel); });
    document.querySelectorAll('#delete-channel').forEach(channel => { channel.addEventListener('click', deleteChannel); });
}

async function addChannel() {
    //POST request content formatting
    const channeName = document.getElementById('id_channel_name').value;
    const channelGroup = document.getElementById('id_channel_group').value;
    const content = `{"channel_name": "${channeName}", "channel_group": "${channelGroup}"}`;
    //POST request
    const CSRFToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const URL = '/dashboard/add-channel';
    const response = await fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFToken,
            'origin': CSRFToken
        },
        body: content
    });
    let HTMLresponse = await response.text();
    //Fetch.Response insertion in sources pannel
    const sourceDetail = document.getElementById('source-list');
    sourceDetail.innerHTML = HTMLresponse;
    document.querySelectorAll('.form-check-input').forEach(toggle => { toggle.addEventListener('click', toggleChannelGroup); });
    document.querySelectorAll('#channel').forEach(channel => { channel.addEventListener('click', toggleChannel); });
    document.querySelectorAll('#delete-channel').forEach(channel => { channel.addEventListener('click', deleteChannel); });
    document.getElementById('id_channel_name').attributes.value = '';
}

async function createFilter() {
    //POST request content formatting
    const textFilter = document.getElementById('id_text_filter').value;
    const translationFilter = document.getElementById('id_translation_filter').value
    const vviewCountFilter = document.getElementById('id_view_count').value
    const shareCountFilter = document.getElementById('id_share_count').value
    const startDate = document.getElementById('id_start_date').value
    const endDate = document.getElementById('id_end_date').value
    const content = `{"text_filter": "${textFilter}", "translation_filter": "${translationFilter}", "view_count": "${vviewCountFilter}", "share_count": "${shareCountFilter}", "start_date": "${startDate}", "end_date": "${endDate}"}`;
    //POST request
    const CSRFToken = document.getElementsByName("csrfmiddlewaretoken")[1].value;
    const URL = '/dashboard/create-filter';
    const response = await fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFToken,
            'origin': CSRFToken
        },
        body: content
    });
    let HTMLresponse = await response.text();
    //Fetch.Response insertion in filter detail pannel
    const filterDetail = document.getElementById('filter-detail');
    filterDetail.innerHTML = HTMLresponse;
    document.querySelectorAll('#toggle-filter').forEach(filter => { filter.addEventListener('click', toggleFilter); });
    document.querySelectorAll('#delete-filter').forEach(filter => { filter.addEventListener('click', deleteFilter); });
}

function toggleFilter(e) {
    //Request filter toggle to Django dashboard/views
    const filter = e.target.attributes.value.nodeValue;
    const filterDetail = document.getElementById('filter-detail');
    const request = `/dashboard/toggle-filter/${filter}`;
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    filterDetail.innerHTML = xmlHttp.responseText;
    document.querySelectorAll('#toggle-filter').forEach(filter => { filter.addEventListener('click', toggleFilter); });
    document.querySelectorAll('#delete-filter').forEach(filter => { filter.addEventListener('click', deleteFilter); });
    updateMessages();
    computeGraph()
}

function deleteFilter(e) {
    //Request filter toggle to Django dashboard/views
    const filter = e.target.attributes.value.nodeValue;
    const request = `/dashboard/delete-filter/${filter}`;
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    const filterDetail = document.getElementById('filter-detail');
    filterDetail.innerHTML = xmlHttp.responseText;
    document.querySelectorAll('#toggle-filter').forEach(filter => { filter.addEventListener('click', toggleFilter); });
    document.querySelectorAll('#delete-filter').forEach(filter => { filter.addEventListener('click', deleteFilter); });
    updateMessages();
    computeGraph();
}

function updateMessages() {
    //Update message thread according to selected filters
    const xmlHttp = new XMLHttpRequest();
    const request = `/dashboard/update-messages`;
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    const messageThread = document.getElementById('messages');
    messageThread.innerHTML = xmlHttp.responseText;
    document.getElementById('sort-by-date').addEventListener('click', function() { sortByDate(); });
    document.querySelectorAll('#message-container').forEach(message => { message.addEventListener('click', showDetail); });
}

function sortByDate() {
    //Request to Django to sort message thread up or down
    const messageThread = document.getElementById('messages');
    const request = '/dashboard/sort-by-date';
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    messageThread.innerHTML = xmlHttp.responseText;
    document.getElementById('sort-by-date').addEventListener('click', function() { sortByDate(); });
    document.querySelectorAll('#message-container').forEach(message => { message.addEventListener('click', showDetail); });
}

function showDetail(e) {
    //Open detail panel if closed
    const detailPanel = document.getElementById('details')
    const separator = detailPanel.nextElementSibling;
    if (detailPanel.attributes.class.value == "d-none flex-column align-items-stretch flex-shrink-0 bg-white p-3 resizable") {
        separator.setAttribute("class", "d-block b-example-divider b-example-vr");
        detailPanel.setAttribute("class", "d-flex flex-column align-items-stretch flex-shrink-0 bg-white p-3 resizable");
    }
    //Show detailed message in the detail panel
    const index = e.target.attributes.value.nodeValue;
    const request = `/dashboard/get-message-detail/${index}`;
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    const messageDetail = document.getElementById('message-detail');
    messageDetail.innerHTML = xmlHttp.responseText;
}


function graphSelect(e) {
    const selection = e.target.value;
    const target = e.target.parentElement.nextElementSibling;
    console.log(target);
    if (selection == 1) {
        postTimeline(target);
    }
}


function postTimeline(target) {
    //Compute and display a graph from filtered messages
    //Data parsing
    target.innerHTML = ''

    //Data parsing
    const data = getFilteredData();
    const values = JSON.parse(data);
    const formatTime = d3.timeFormat("%Y.%m.%d");
    const tally = {};
    const dataset = [];
    values.forEach(function(line) {
        const datetime = d3.isoParse(line.fields.message_date);
        const date = formatTime(datetime);
        tally[date] = (tally[date]||0) + 1;
    });
    for (const date in tally) {
        if (tally.hasOwnProperty(date)) {
            dataset.push({
                date: date,
                frequency: tally[date]
            });
        }
    }

    //Post timeline layout from d3.js
    const canvas = target;
    const canvasWidth = canvas.offsetWidth;
    const canvasHeight = canvas.offsetHeight / 1.15;
    const margin = {top: 20, right: 80, bottom: 70, left: 30};
    const width = canvasWidth - margin.left - margin.right;
    const height = canvasHeight - margin.top - margin.bottom;

    var svg = d3.select(canvas)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
        // X axis
        var x = d3.scaleTime()
            .domain(d3.extent(dataset, function(d) { return new Date(d.date); }))
            .range([0, width]);
        var xAxis = d3.axisBottom(x)
            .ticks(d3.timeDay)
            .tickFormat(d3.timeFormat("%Y.%m.%d"));
        svg.append("g")
            .attr("transform", "translate(0, " + height + ")")
            .call(xAxis)
            .selectAll('line')
                .attr("transform", "translate(" + (width / dataset.length * 0.35) + ", 0)");
        svg.selectAll("text")
            .attr("transform", "translate(0, 10)rotate(-90)")
            .attr("class", "smaller")
            .style("text-anchor", "end")
            .style("font-family", "");
        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, Math.round(d3.max(dataset, function(d) { return d.frequency }))*1.1])
            .range([height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y))
            .selectAll("text")
                .style("font-family", "")
        //Add bars
        svg.selectAll("mybar")
            .data(dataset)
            .enter()
            .append("rect")
                .attr("x", function(d) { return x(new Date(d.date)); })
                .attr("y", function(d) { return y(d.frequency); })
                .attr("width", width / dataset.length * 0.7)
                .attr("height", function(d) { return height - y(d.frequency); })
                .attr("fill", "#838383")
}

function viewTimeline(target) {
    //Compute and display a graph from filtered messages
    //Data parsing
    target.innerHTML = ''

    //Data parsing
    const data = getFilteredData();
    const values = JSON.parse(data);
    const formatTime = d3.timeFormat("%Y.%m.%d");
    const tally = {};
    const dataset = [];
    values.forEach(function(line) {
        console.log(line.fields.view_count)
        const datetime = d3.isoParse(line.fields.message_date);
        const date = formatTime(datetime);
        tally[date] = (tally[date]||0) + line.fields.view_count;
    });
    for (const date in tally) {
        if (tally.hasOwnProperty(date)) {
            dataset.push({
                date: date,
                frequency: tally[date]
            });
        }
    }

    //Post timeline layout from d3.js
    const canvas = target;
    const canvasWidth = canvas.offsetWidth;
    const canvasHeight = canvas.offsetHeight / 1.15;
    const margin = {top: 20, right: 80, bottom: 70, left: 30};
    const width = canvasWidth - margin.left - margin.right;
    const height = canvasHeight - margin.top - margin.bottom;

    var svg = d3.select(canvas)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
        // X axis
        var x = d3.scaleTime()
            .domain(d3.extent(dataset, function(d) { return new Date(d.date); }))
            .range([0, width]);
        var xAxis = d3.axisBottom(x)
            .ticks(d3.timeDay)
            .tickFormat(d3.timeFormat("%Y.%m.%d"));
        svg.append("g")
            .attr("transform", "translate(0, " + height + ")")
            .call(xAxis)
            .selectAll('line')
                .attr("transform", "translate(" + (width / dataset.length * 0.35) + ", 0)");
        svg.selectAll("text")
            .attr("transform", "translate(0, 10)rotate(-90)")
            .attr("class", "smaller")
            .style("text-anchor", "end")
            .style("font-family", "");
        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, Math.round(d3.max(dataset, function(d) { return d.frequency }))*1.1])
            .range([height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y))
            .selectAll("text")
                .style("font-family", "")
                .format(".2s");
        //Add bars
        svg.selectAll("mybar")
            .data(dataset)
            .enter()
            .append("rect")
                .attr("x", function(d) { return x(new Date(d.date)); })
                .attr("y", function(d) { return y(d.frequency); })
                .attr("width", width / dataset.length * 0.7)
                .attr("height", function(d) { return height - y(d.frequency); })
                .attr("fill", "#838383")
}

function addEvents() {
    //Event listeners
    //Nav bar toggles
    document.getElementById('nav-general').addEventListener('click', function() { toggleAllPanels(); });
    document.getElementById('nav-sources').addEventListener('click', function() { collapse('sources'); });
    document.getElementById('nav-filtres').addEventListener('click', function() { collapse('filtres'); });
    document.getElementById('nav-messages').addEventListener('click', function() { collapse('messages'); });
    document.getElementById('nav-details').addEventListener('click', function() { collapse('details'); });
    document.getElementById('nav-analysis').addEventListener('click', function() { collapse('quantitative-analysis'); computeGraph() });
    document.getElementById('nav-update').addEventListener('click', function() { updateData(); });
    //Channel group toggle
    document.querySelectorAll('.form-check-input').forEach(toggle => { toggle.addEventListener('click', toggleChannelGroup); });
    //Channel toggle
    document.querySelectorAll('#channel').forEach(channel => { channel.addEventListener('click', toggleChannel); });
    //Channel delete
    document.querySelectorAll('#delete-channel').forEach(channel => { channel.addEventListener('click', deleteChannel); });
    //Add channel
    document.getElementById('add-channel-button').addEventListener('click', function() { addChannel(); });
    //Create filter
    document.getElementById('create-filter-button').addEventListener('click', function() { createFilter(); });
    //Filter toggle
    document.querySelectorAll('#toggle-filter').forEach(filter => { filter.addEventListener('click', toggleFilter); });
    //Delete filter
    document.querySelectorAll('#delete-filter').forEach(filter => { filter.addEventListener('click', deleteFilter); });
    //Sort by date button
    document.getElementById('sort-by-date').addEventListener('click', function() { sortByDate(); });
    //Message detail toggle
    document.querySelectorAll('#message-container').forEach(message => { message.addEventListener('click', showDetail); });
    //Graph selection
    document.querySelectorAll('#graph-selection').forEach(message => { message.addEventListener('click', graphSelect); });
    //Graph Panel resize event
    document.getElementById('quantitative-analysis').addEventListener('click', function() { postTimeline(); });

}

addEvents();
const target = document.getElementById("graph-3");
viewTimeline(target);