
function addNode(parentId, nodeId, nodeLable, position) {
  var panel = d3.select("#" + parentId);
  panel.append('div').style('width','120px').style('height','50px')
    .style('position','absolute')
    .style('top',position.y).style('left',position.x)
    .style('border','2px #9DFFCA solid').attr('align','center')
    .attr('id',nodeId).classed('node',true)
    .text(nodeLable);

    //设置双击删除节点
    // document.getElementById(nodeId).ondblclick=function(){
    //   document.getElementById(nodeId).remove()
    // }
  return jsPlumb.getSelector('#' + nodeId)[0];
}

function addPorts(instance, node, ports, type) {
  //Assume horizental layout
  var number_of_ports = ports.length;
  var i = 0;
  var height = $(node).height();  //Note, jquery does not include border for height
  var y_offset = 1 / ( number_of_ports + 1);
  var y = 0;

  for ( ; i < number_of_ports; i++ ) {
    var anchor = [0,0,0,0];
    var paintStyle = { radius:5, fillStyle:'#FF8891' };
    var isSource = false, isTarget = false;
    if ( type === 'output' ) {
      anchor[0] = 1;
      paintStyle.fillStyle = '#051bfa';
      isSource = true;
    } else {
      isTarget =true;
    }

    anchor[1] = y + y_offset;
    y = anchor[1];

    instance.addEndpoint(node, {
      uuid:node.getAttribute("id") + "-" + ports[i],
      paintStyle: paintStyle,
      anchor:anchor,
      maxConnections:-1,
      isSource:isSource,
      isTarget:isTarget
    });

  }
}

function connectPorts(instance, node1, port1, node2 , port2) {
  // declare some common values:
  var color = "gray";
  var arrowCommon = { foldback:0.8, fillStyle:color, width:5 },
  // use three-arg spec to create two different arrows with the common values:
  overlays = [
    [ "Arrow", { location:0.8 }, arrowCommon ],
    [ "Arrow", { location:0.2, direction:-1 }, arrowCommon ]
  ];

  var uuid_source = node1.getAttribute("id") + "-" + port1;
  var uuid_target = node2.getAttribute("id") + "-" + port2;

  instance.connect({uuids:[uuid_source, uuid_target]});
}

jsPlumb.ready(function() {
    console.log("jsPlumb is ready to use");

    //Initialize JsPlumb
    var color = "#E8C870";
    var instance = jsPlumb.getInstance({
      // notice the 'curviness' argument to this Bezier curve.  the curves on this page are far smoother
      // than the curves on the first demo, which use the default curviness value.
      Connector : [ "Bezier", { curviness:50 } ],
      DragOptions : { cursor: "pointer", zIndex:2000 },
      PaintStyle : { strokeStyle:color, lineWidth:2 },
      EndpointStyle : { radius:5, fillStyle:color },
      HoverPaintStyle : {strokeStyle:"#7073EB" },
      EndpointHoverStyle : {fillStyle:"#7073EB" },
      Container:"flow-panel"
    });

    //产生坐标值 会在产生后增加 避免全覆盖
    var dx = 180;
    var dy = 180;

    // 设置单击产生元件
    document.getElementById("and").onclick=function(){
      var uid = new Date().getTime();
      var mx = ''+dx+'px';
      var my = ''+dy+'px';
      dx += 10;
      dy += 10;
      var node = addNode('flow-panel','node' + uid, "AND", {x:mx,y:my});
      addPorts(instance, node, ['out1'],'output');
      addPorts(instance, node, ['in1','in2'],'input')
      instance.draggable($(node));
    }
    document.getElementById("or").onclick=function(){
      var uid = new Date().getTime();
      var mx = ''+dx+'px';
      var my = ''+dy+'px';
      dx += 10;
      dy += 10;
      var node = addNode('flow-panel','node' + uid, "OR", {x:mx,y:my});
      addPorts(instance, node, ['out1'],'output');
      addPorts(instance, node, ['in1','in2'],'input')
      instance.draggable($(node));
    }
    document.getElementById("xor").onclick=function(){
      var uid = new Date().getTime();
      var mx = ''+dx+'px';
      var my = ''+dy+'px';
      dx += 10;
      dy += 10;
      var node = addNode('flow-panel','node' + uid, "XOR", {x:mx,y:my});
      addPorts(instance, node, ['out1'],'output');
      addPorts(instance, node, ['in1','in2'],'input')
      instance.draggable($(node));
    }
    document.getElementById("not").onclick=function(){
      var uid = new Date().getTime();
      var mx = ''+dx+'px';
      var my = ''+dy+'px';
      dx += 10;
      dy += 10;
      var node = addNode('flow-panel','node' + uid, "NOT", {x:mx,y:my});
      addPorts(instance, node, ['out1'],'output');
      addPorts(instance, node, ['in1','in2'],'input')
      instance.draggable($(node));
    }


    $('#flow-panel').on('drop', function(ev){
      //avoid event conflict for jsPlumb
      if (ev.target.className.indexOf('_jsPlumb') >= 0 ) {
        return;
      }

      ev.preventDefault();
      var mx = '' + ev.originalEvent.offsetX + 'px';
      var my = '' + ev.originalEvent.offsetY + 'px';

      console.log('on drop : ' + ev.originalEvent.dataTransfer.getData('text'));
      var text = ev.originalEvent.dataTransfer.getData('text');
      var uid = new Date().getTime();
      var node = addNode('flow-panel','node' + uid, text, {x:mx,y:my});
      if(text=="NOT"){
        addPorts(instance, node, ['out'],'output');
        addPorts(instance, node, ['in1'],'input');
      }
      else{
        addPorts(instance, node, ['out'],'output');
        addPorts(instance, node, ['in1'],'input');
      }
      instance.draggable($(node));
    }).on('dragover', function(ev){
      ev.preventDefault();
      console.log('on drag over');
    });

    instance.doWhileSuspended(function() {
      // declare some common values:
      var arrowCommon = { foldback:0.8, fillStyle:color, width:5 },
      // use three-arg spec to create two different arrows with the common values:
      overlays = [
        [ "Arrow", { location:0.8 }, arrowCommon ],
        [ "Arrow", { location:0.2, direction:-1 }, arrowCommon ]
      ];

      var inNum = parseInt(document.getElementById("inputNum").innerHTML);
      var aswNum = parseInt(document.getElementById("aswNum").innerHTML);
      var Ix = (document.getElementById("inputPortsList").value);
      var Ay = (document.getElementById("aswPortsList").value);
      var inPortList = Ix.split(' ')
      var aswPortList = Ay.split(' ')
      var dy = 20;
      for (var i = 0; i<inNum;i++){
        my = ''+dy+'px';
        var node = addNode('flow-panel','nodeInput'+i,inPortList[i],{x:'0px',y:my});
        dy += (parseInt(500/inNum));
        addPorts(instance, node, ['out1'],'output');
        //document.getElementById("nodeInput"+i).draggable = true
      }

      dy = 20;
      for (var i = 0; i<aswNum;i++){
        my = ''+dy+'px';
        var node = addNode('flow-panel','nodeOut'+i,aswPortList[i],{x:'700px',y:my});
        dy += (parseInt(500/inNum));
        addPorts(instance, node, ['in1'],'input');
      }

      instance.draggable($('.node'));

    });

    jsPlumb.fire("jsFlowLoaded", instance);

});

