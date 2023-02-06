//Find message from its .models.Message db id (pk)
function retrieveMessage(index) {
    for (const d of data) {
        if (d.pk == index) {
            return d;
        }
    }
}

//Show all panels from "Vue générale"
function toggleAllPanels() {
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

//Toggle panels from nav bar depending on selected id
function collapse(id) {
    const targetElement = document.getElementById(id);
    const separator = targetElement.nextElementSibling;
    if (targetElement.attributes.class.value == "d-flex flex-column flex-shrink-0 p-3 bg-light") {
        separator.setAttribute("class", "d-none b-example-divider b-example-vr");
        targetElement.setAttribute("class", "d-none flex-column flex-shrink-0 p-3 bg-light");
    } else if (targetElement.attributes.class.value == "d-flex flex-column align-items-stretch flex-shrink-0 bg-white p-3") {
        separator.setAttribute("class", "d-none b-example-divider b-example-vr");
        targetElement.setAttribute("class", "d-none flex-column align-items-stretch flex-shrink-0 bg-white p-3");
    } else if (targetElement.attributes.class.value == "d-none flex-column flex-shrink-0 p-3 bg-light") {
        separator.setAttribute("class", "d-block b-example-divider b-example-vr");
        targetElement.setAttribute("class", "d-flex flex-column flex-shrink-0 p-3 bg-light");
    } else if (targetElement.attributes.class.value == "d-none flex-column align-items-stretch flex-shrink-0 bg-white p-3") {
        separator.setAttribute("class", "d-block b-example-divider b-example-vr");
        targetElement.setAttribute("class", "d-flex flex-column align-items-stretch flex-shrink-0 bg-white p-3");
    }
}

function updateData() {
    const request = '/dashboard/update-data';
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    const messageThread = document.getElementById('message-thread');
    messageThread.innerHTML = xmlHttp.responseText;
}

//Request channel group toggle to Django dashboard/views
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
}

//Request channel toggle to Django dashboard/views
function toggleChannel(e) {
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

function addChannel() {
    const request = '/dashboard/add-channel/';
    const channeName = document.getElementById('id_channel_name').value;
    const channelGroup = document.getElementById('id_channel_group').value;
    const content = [];
    content.push(`${encodeURIComponent(channeName)}=${encodeURIComponent(channelGroup)}`);
    const encodedContent = content.join('&').replace(/%20/g, '+');
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", request, false);
    xmlHttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlHttp.send( encodedContent );
}

//Request filter toggle to Django dashboard/views
function toggleFilter(e) {
    const filter = e.target.attributes.value.nodeValue;
    const filterDetail = document.getElementById('filter-detail');
    const request = `/dashboard/toggle-filter/${filter}`;
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    filterDetail.innerHTML = xmlHttp.responseText;
    document.querySelectorAll('#filter').forEach(filter => { filter.addEventListener('click', toggleFilter); });
    updateMessages();
}

//Update message thread according to selected filters
function updateMessages() {
    const messageThread = document.getElementById('message-thread');
    const xmlHttp = new XMLHttpRequest();
    const request = `/dashboard/update-messages`;
    xmlHttp.open("GET", request, false);
    xmlHttp.send( null );
    messageThread.innerHTML = xmlHttp.responseText;
    document.querySelectorAll('#message-container').forEach(message => { message.addEventListener('click', showDetail); });
}

//Show detailed message in the detail panel by loading JSON data from .view JSON serializer
function showDetail(e) {
    const index = e.target.attributes.value.nodeValue;
    const message = retrieveMessage(index);
    const detail = document.getElementById('message-detail');
    const messageDate = new Date(message.fields.message_date).toLocaleString();
    const detailTemplate = `<div class="list-group-item py-3 lh-sm" id="message-container" aria-current="true"><div class="d-flex w-100 align-items-center justify-content-between"><strong class="mb-1 text-truncate">${message.fields.channel_name}</strong><a href="https://t.me/${message.fields.channel_name}/${message.fields.message_id}" class="text-muted text-decoration-none"><small class="text-muted">${messageDate}</small></a></div><span class="d-flex align-items-center justify-content-end"><div class="text-muted small me-1">${message.fields.view_count}</div><img class="bi pe-none me-2" width="12" height="12" src="/static/dashboard/images/views.svg" style="filter: invert(1);"><div class="text-muted small me-1">${message.fields.share_count}</div><img class="bi pe-none" width="12" height="12" src="/static/dashboard/images/shares.svg" style="filter: invert(1);"></span><div class="mt-3 mb-3 smaller">${message.fields.message_text}</div><div class="mb-3 small text-muted fst-italic smaller">Traduction : ${message.fields.text_translation}</div></div>`
    detail.innerHTML = detailTemplate;
}

//Event listeners
function addEvents() {
    //Nav bar toggles
    document.getElementById('nav-general').addEventListener('click', function() { toggleAllPanels(); });
    document.getElementById('nav-sources').addEventListener('click', function() { collapse('sources'); });
    document.getElementById('nav-filtres').addEventListener('click', function() { collapse('filtres'); });
    document.getElementById('nav-messages').addEventListener('click', function() { collapse('messages'); });
    document.getElementById('nav-details').addEventListener('click', function() { collapse('details'); });
    document.getElementById('nav-update').addEventListener('click', function() { updateData(); });
    //Message detail toggle
    document.querySelectorAll('#message-container').forEach(message => { message.addEventListener('click', showDetail); });
    //Channel group toggle
    document.querySelectorAll('.form-check-input').forEach(toggle => { toggle.addEventListener('click', toggleChannelGroup); });
    //Channel toggle
    document.querySelectorAll('#channel').forEach(channel => { channel.addEventListener('click', toggleChannel); });
    //Channel delete
    document.querySelectorAll('#delete-channel').forEach(channel => { channel.addEventListener('click', deleteChannel); });
    //Add channel
    document.getElementById('add-channe-button').addEventListener('click', function() { addChannel(); });
    //Filter toggle
    document.querySelectorAll('#filter').forEach(filter => { filter.addEventListener('click', toggleFilter); });
}

addEvents();