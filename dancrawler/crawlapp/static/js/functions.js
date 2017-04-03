document.getElementById("maintitle").innerHTML = "Dan's Crawlerino";

function show(id) {
	var trumpid = "trump" + id
	var div = document.getElementById(trumpid);
	if (div.style.display !== 'none') {
		div.style.display = 'none';
	} else {
		div.style.display = 'block';
	}
}