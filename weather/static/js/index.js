function setup() {
    var url = new URL(window.location.href);
    var lat = url.searchParams.get("lat");
    var lon = url.searchParams.get("lon");

    if (lat && lon) {
        // The server side rendering has handled the weather stuff, we can chill

        return;
    }

    navigator.geolocation.getCurrentPosition((position) => {
        var spinner = document.getElementById("spinner");

        spinner.hidden = true;

        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        var url = "?lat=" + lat + "&lon=" + lon;

        // reload current page with new url
        window.location.href += url;
    }, (error) => {
        console.log("Error from geolocation API: " + error.message);
    });
}

setup();