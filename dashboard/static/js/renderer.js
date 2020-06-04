(function(){

  Renderer = function(canvas){
    var canvas = $(canvas).get(0)
    var ctx = canvas.getContext("2d");
    var gfx = arbor.Graphics(canvas)
    var particleSystem = null
    dom = $(canvas)

    var that = {
      init:function(system){
        particleSystem = system
        particleSystem.screenSize(canvas.width, canvas.height)
        particleSystem.screenPadding(40)
        that.initMouseHandling()
      },

      redraw:function(){
        if (!particleSystem) return

        gfx.clear() // convenience ƒ: clears the whole canvas rect

        // draw the nodes & save their bounds for edge drawing
        var nodeBoxes = {}
        particleSystem.eachNode(function(node, pt){
          // node: {mass:#, p:{x,y}, name:"", data:{}}
          // pt:   {x:#, y:#}  node position in screen coords

          // determine the box size and round off the coords if we'll be
          // drawing a text label (awful alignment jitter otherwise...)
          var label = node.data.label||""

          if (node.data.label == "Gio-Vase")
              var w = ctx.measureText(""+label).width + 60
          else {
            if (node.data.shape=='dot') {
              var w = ctx.measureText("" + label).width + 20
            } else {
               var w = ctx.measureText("" + label).width + 20
            }
          }

          if (!(""+label).match(/^[ \t]*$/)){
            pt.x = Math.floor(pt.x)
            pt.y = Math.floor(pt.y)
          }else{
            label = null
          }

          // draw a rectangle centered at pt
          if (node.data.color) ctx.fillStyle = node.data.color
          else ctx.fillStyle = "rgba(0,0,0,.2)"
          if (node.data.color=='none') ctx.fillStyle = "white"

          if (node.data.shape=='dot'){
            gfx.oval(pt.x-w/2, pt.y-w/2, w,w, {fill:ctx.fillStyle})
            nodeBoxes[node.name] = [pt.x-w/2, pt.y-w/2, w,w]
          }else{
            gfx.rect(pt.x-w/2, pt.y-10, w,30, 10, {fill:ctx.fillStyle})
            nodeBoxes[node.name] = [pt.x-w/2, pt.y-11, w+10, 32]
          }

          // draw the text
          if (label){

            ctx.textAlign = "center"
            ctx.fillStyle = "black"
            ctx.font = "14px Helvetica"
            if (node.data.color=='none') ctx.fillStyle = '#333333'
            if (node.data.shape=='dot'){
                if (node.data.label == "Gio-Vase"){
                  ctx.font = "16px Helvetica"
                }
                ctx.fillStyle = "white"
                ctx.fillText(label||"", pt.x, pt.y+4)
            } else {
              ctx.fillText(label||"", pt.x, pt.y+10)
            }
          }
        })

         // draw the edges
        particleSystem.eachEdge(function(edge, pt1, pt2){
          // edge: {source:Node, target:Node, length:#, data:{}}
          // pt1:  {x:#, y:#}  source position in screen coords
          // pt2:  {x:#, y:#}  target position in screen coords

          var weight = edge.data.weight
          var color = edge.data.color

          if (!color || (""+color).match(/^[ \t]*$/)) color = null

          // find the start point
          var tail = intersect_line_box(pt1, pt2, nodeBoxes[edge.source.name])
          var head = intersect_line_box(tail, pt2, nodeBoxes[edge.target.name])

          ctx.save()
            ctx.beginPath()
            ctx.lineWidth = (!isNaN(weight)) ? parseFloat(weight) : 1
            ctx.strokeStyle = (color) ? color : "#cccccc"
            ctx.fillStyle = null

            ctx.moveTo(tail.x, tail.y)
            ctx.lineTo(head.x, head.y)
            ctx.stroke()
          ctx.restore()

          // draw an arrowhead if this is a -> style edge
          if (edge.data.directed){
            ctx.save()
              // move to the head position of the edge we just drew
              var wt = !isNaN(weight) ? parseFloat(weight) : 1
              var arrowLength = 6 + wt
              var arrowWidth = 2 + wt
              ctx.fillStyle = (color) ? color : "#cccccc"
              ctx.translate(head.x, head.y);
              ctx.rotate(Math.atan2(head.y - tail.y, head.x - tail.x));

              // delete some of the edge that's already there (so the point isn't hidden)
              ctx.clearRect(-arrowLength/4,-wt/4, arrowLength/4,wt/2)

              // draw the chevron
              ctx.beginPath();
              ctx.moveTo(-arrowLength, arrowWidth);
              ctx.lineTo(0, 0);
              ctx.lineTo(-arrowLength, -arrowWidth);
              ctx.lineTo(-arrowLength * 0.9, -0);
              ctx.closePath();
              ctx.fill();
            ctx.restore()
          }
        })
      },
      initMouseHandling:function(){
        // no-nonsense drag and drop (thanks springy.js)
      	selected = null;
      	nearest = null;
      	var dragged = null;
        var oldmass = 1

        $(canvas).mousedown(function(e){
      		var pos = $(this).offset();
      		var p = {x:e.pageX-pos.left, y:e.pageY-pos.top}
      		selected = nearest = dragged = particleSystem.nearest(p);
      		if (selected.node !== null) {
              dragged.node.tempMass = 50
              dragged.node.fixed = true
            }
      		return false
      	});

        $(canvas).dblclick(function (e) {
          var pos = $(this).offset();
          var p = {x:e.pageX-pos.left, y:e.pageY-pos.top}
          selected = nearest = dragged = particleSystem.nearest(p);
          if (selected.node !== null){
              if (selected.node.data.l !== 'no'){
                 dom.addClass('linkable')
                 window.open(selected.node.data.link);
              }
              else
                 dom.removeClass('linkable')
          }
          return false
        })

      	$(canvas).mousemove(function(e){
          var old_nearest = nearest && nearest.node._id
      		var pos = $(this).offset();
      		var s = {x:e.pageX-pos.left, y:e.pageY-pos.top};

      		nearest = particleSystem.nearest(s);
          if (!nearest) return

      		if (dragged !== null && dragged.node !== null){
            var p = particleSystem.fromScreen(s)
      			dragged.node.p = {x:p.x, y:p.y}
            // dragged.tempMass = 10000
      		}

          return false
      	});

      	$(window).bind('mouseup',function(e){
          if (dragged===null || dragged.node===undefined) return
          dragged.node.fixed = false
          dragged.node.tempMass = 100
          dragged = null;
          selected = null
          return false
      	});

      } //end handling

    }

    // helpers for figuring out where to draw arrows (thanks springy.js)
    var intersect_line_line = function(p1, p2, p3, p4)
    {
      var denom = ((p4.y - p3.y)*(p2.x - p1.x) - (p4.x - p3.x)*(p2.y - p1.y));
      if (denom === 0) return false // lines are parallel
      var ua = ((p4.x - p3.x)*(p1.y - p3.y) - (p4.y - p3.y)*(p1.x - p3.x)) / denom;
      var ub = ((p2.x - p1.x)*(p1.y - p3.y) - (p2.y - p1.y)*(p1.x - p3.x)) / denom;

      if (ua < 0 || ua > 1 || ub < 0 || ub > 1)  return false
      return arbor.Point(p1.x + ua * (p2.x - p1.x), p1.y + ua * (p2.y - p1.y));
    }

    var intersect_line_box = function(p1, p2, boxTuple)
    {
      var p3 = {x:boxTuple[0], y:boxTuple[1]},
          w = boxTuple[2],
          h = boxTuple[3]

      var tl = {x: p3.x, y: p3.y};
      var tr = {x: p3.x + w, y: p3.y};
      var bl = {x: p3.x, y: p3.y + h};
      var br = {x: p3.x + w, y: p3.y + h};

      return intersect_line_line(p1, p2, tl, tr) ||
            intersect_line_line(p1, p2, tr, br) ||
            intersect_line_line(p1, p2, br, bl) ||
            intersect_line_line(p1, p2, bl, tl) ||
            false
    }

    return that
  }

})()