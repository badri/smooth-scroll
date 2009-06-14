
            // constants
            var viewportWidth = 800; // dummy values
            var viewportHeight = 600; // dummy values
            var tileSize = 100;
            // START:globalstate
            var zoom = 0;
            var zoomSizes = [ [ "2000px", "1400px" ], [ "1500px", "1050px" ] ];
            // END:globalstate

            // used to control moving the map div
            var dragging = false;
            var top;
            var left;
            var dragStartTop;
            var dragStartLeft;

	    var dragx = false;
            var dragy = false;

            function init() {
                // make inner div big enough to display the map
                // START:innerDivSize
                setInnerDivSize(zoomSizes[zoom][0], zoomSizes[zoom][1]);
                // END:innerDivSize

                // wire up the mouse listeners to do dragging
                var outerDiv = document.getElementById("outerDiv");
                outerDiv.onmousedown = startMove;
                outerDiv.onmousemove = processMove;
                outerDiv.onmouseup = stopMove;

                // necessary to enable dragging on IE
                outerDiv.ondragstart = function() { return false; }

                checkTiles();
            }

            function startMove(event) {
                // necessary for IE
                if (!event) event = window.event;
                dragStartLeft = event.clientX;
                dragStartTop = event.clientY;
                var innerDiv = document.getElementById("innerDiv");
                innerDiv.style.cursor = "-moz-grab";

                top = stripPx(innerDiv.style.top);
                left = stripPx(innerDiv.style.left);

                dragging = true;
	        dragx = true;
	        dragy = true;
                return false;
            }

            function processMove(event) {
                if (!event) event = window.event;  // for IE
                var innerDiv = document.getElementById("innerDiv");
                if (dragging) {
                    if(dragy)
		      {
		        innerDiv.style.top = top + (event.clientY - dragStartTop);
			top_limit = viewportWidth - innerDiv.style.height;
			if(stripPx(innerDiv.style.top) < top_limit)
			  innerDiv.style.top = top_limit;
			if(stripPx(innerDiv.style.top) > 0)
			  innerDiv.style.top = 10;
		      }
                    if(dragx)
		      {
			innerDiv.style.left = left + (event.clientX - dragStartLeft);
			left_limit = viewportWidth - innerDiv.style.width;
			if(stripPx(innerDiv.style.left) < left_limit)
			  innerDiv.style.left = left_limit;
			if(stripPx(innerDiv.style.left) > 0)
			  innerDiv.style.left = 10;
		      }
                }

              checkTiles();
            }
            // START:checktiles
            function checkTiles() {
                // check which tiles should be visible in the inner div
                var visibleTiles = getVisibleTiles();

                // add each tile to the inner div, checking first to see
                // if it has already been added
                var innerDiv = document.getElementById("innerDiv");
                var visibleTilesMap = {};
                for (i = 0; i < visibleTiles.length; i++) {
                    var tileArray = visibleTiles[i];
                    // START:imgZoomLevel
		  if(tileArray[0]>(stripPx(zoomSizes[zoom][0])/100 - 1) || tileArray[0]<0) dragx = false;
		  if(tileArray[1]>(stripPx(zoomSizes[zoom][0])/100 - 1)  || tileArray[0]<0) dragy = false;

                    var tileName = "x" + tileArray[0] + "y" + tileArray[1] + "z" + zoom;
                    // END:imgZoomLevel
                    visibleTilesMap[tileName] = true;
                    var img = document.getElementById(tileName);
                    if (!img) {
                        img = document.createElement("img");
                        img.src = "resources/tiles/" + tileName + ".jpg";
                        img.style.position = "absolute";
                        img.style.left = (tileArray[0] * tileSize) + "px";
                        img.style.top = (tileArray[1] * tileSize) + "px";
                        img.style.zIndex = 0;
                        img.setAttribute("id", tileName);
		      if(stripPx(img.style.top)<=(stripPx(zoomSizes[zoom][1])-100) && stripPx(img.style.left)<=(stripPx(zoomSizes[zoom][0])-100))
		      // if(stripPx(img.style.top)<=1300 && stripPx(img.style.left)<=1900)
                        innerDiv.appendChild(img);
                    }
                }

                // START:ignorePushPin
                var imgs = innerDiv.getElementsByTagName("img");
                for (i = 0; i < imgs.length; i++) {
                    var id = imgs[i].getAttribute("id");
                    if (!visibleTilesMap[id]) {
                        if (id != "pushPin") {
                            innerDiv.removeChild(imgs[i]);
                            i--;  // compensate for live nodelist
                        }
                    }
                }
                // END:ignorePushPi
            }
            // END:checktiles

            function getVisibleTiles() {
                var innerDiv = document.getElementById("innerDiv");

                var mapX = stripPx(innerDiv.style.left);
                var mapY = stripPx(innerDiv.style.top);

                var startX = Math.abs(Math.floor(mapX / tileSize)) - 1;
                var startY = Math.abs(Math.floor(mapY / tileSize)) - 1;

                var tilesX = Math.ceil(viewportWidth / tileSize) + 1;
                var tilesY = Math.ceil(viewportHeight / tileSize) + 1;

                var visibleTileArray = [];
                var counter = 0;
                for (x = startX; x < (tilesX + startX); x++) {
                    for (y = startY; y < (tilesY + startY); y++) {
                        visibleTileArray[counter++] = [x, y];
                    }
                }
                return visibleTileArray;
            }


            function stopMove() {
                var innerDiv = document.getElementById("innerDiv");
                innerDiv.style.cursor = "";
                dragging = false;
	      dragx = false;
	      dragy = false;
            }

            function stripPx(value) {
                if (value == "") return 0;
                return parseFloat(value.substring(0, value.length - 2));
            }

            function setInnerDivSize(width, height) {
                var innerDiv = document.getElementById("innerDiv");
                innerDiv.style.width = width;
                innerDiv.style.height = height;
	        var oDiv = document.getElementById("outerDiv");
	      oDiv.style.width = "100%";
	      oDiv.style.height = "100%";
	      viewportWidth = oDiv.offsetWidth;
	      viewportHeight = oDiv.offsetHeight;
            }

            // START:toggleZoom
            function toggleZoom() {
                zoom = (zoom == 0) ? 1 : 0;

                var innerDiv = document.getElementById("innerDiv");
                var imgs = innerDiv.getElementsByTagName("img");
                while (imgs.length > 0) innerDiv.removeChild(imgs[0]);

                setInnerDivSize(zoomSizes[zoom][0], zoomSizes[zoom][1]);

                checkTiles();
            }
            // END:toggleZoom

            // START:togglePushPin
            function togglePushPin() {
                var pinImage = document.getElementById("pushPin");
                if (pinImage) {
                    pinImage.parentNode.removeChild(pinImage);
                    var dialog = document.getElementById("pinDialog");
                    dialog.parentNode.removeChild(dialog);
                    return;
                }

                var innerDiv = document.getElementById("innerDiv");
                pinImage = document.createElement("img");
                pinImage.src = "resources/images/pin.png";
                pinImage.style.position = "absolute";
                pinImage.style.left = (zoom == 0) ? "850px" : "630px";
                pinImage.style.top = (zoom == 0) ? "570px" : "420px";
                pinImage.style.zIndex = 1;
                pinImage.setAttribute("id", "pushPin");
                innerDiv.appendChild(pinImage);

                var dialog = document.createElement("div");
                dialog.style.position = "absolute";
                dialog.style.left = (stripPx(pinImage.style.left) - 90) + "px";
                dialog.style.top = (stripPx(pinImage.style.top) - 210) + "px";
                dialog.style.width = "309px";
                dialog.style.height = "229px";
                dialog.style.backgroundImage = "url(resources/images/dialog.png)";
                dialog.style.zIndex = 2;
                dialog.setAttribute("id", "pinDialog");
                dialog.innerHTML = "<table height='80%' width='100%'>" +
                    "<tr><td align='center'>The capital of Spain</td></tr></table>";
                innerDiv.appendChild(dialog);
            }
            // END:togglePushPin
