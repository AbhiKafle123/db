
var userCircleRadius = 50; 
var nodePositionx = 0;
var nodePositiony = height/2;
// var userProfImageurl = "https://scontent-atl3-1.xx.fbcdn.net/v/t1.0-9/944895_10206276962865501_1284324373444561337_n.jpg?oh=058a568b5799d7e821febd1cf3aaab52&oe=58D524F8"
var userProfImageurl = "https://graph.facebook.com/" + user_data.id +"/picture?type=large&width=1000&height=1000"
// var friendProfImageurl = "https://scontent.xx.fbcdn.net/v/t1.0-9/14695347_10211080020946214_7107138922234443017_n.jpg?oh=f3708b7b41078df2e8ab56773b228352&oe=58958072"
var friendProfImageurl = "https://graph.facebook.com/" + friend_data.id +"/picture?type=large&width=1000&height=1000"
console.log(userProfImageurl);

var userProfileImage = svg.append("defs")
                    .append("pattern")
                      .attr("id", "userProfileImage")
                      .attr("height", 1)
                      .attr("width", 1)
                      .append("image")
                        .attr("height", userCircleRadius *2)
                        .attr("width", userCircleRadius *2)
                        .attr("xlink:href", userProfImageurl)


var friendProfileImage = svg.append("defs")
                    .append("pattern")
                      .attr("id", "friendProfileImage")
                      .attr("height", 1)
                      .attr("width", 1)
                      .append("image")
                        .attr("height", userCircleRadius*2)
                        .attr("width", userCircleRadius *2)
                        .attr("xlink:href", friendProfImageurl)


var user = svg.append("g")
                .attr("transform", function(d){return "translate(-200,-200)"; });

var userPic = user.append("circle")
                  .attr("cx", nodePositionx)
                  .attr("cy", nodePositiony)
                  .attr("r",userCircleRadius)
                  .attr("stroke", "blue")
                  .attr("fill","transparent")
                  .style("fill", "url(#userProfileImage)")
                  
var userName = user.append("text")
                    .attr("dx", nodePositionx)
                    .attr("dy", nodePositiony)
                    .attr("text-anchor","middle")
                    .text(user_data.name)
                    .attr("transform", function(d){return "translate(0,"+(userCircleRadius+20)+")"; });

var friend = svg.append("g")
                .attr("transform", function(d){return "translate(-200,200)"; });

var friendPic = friend.append("circle")
                .attr("cx", nodePositionx)
                .attr("cy", nodePositiony)
                .attr("r",userCircleRadius)
                .attr("stroke", "blue")
                .attr("fill","transparent")
                .style("fill", "url(#friendProfileImage)")

var userName = friend.append("text")
                    .attr("dx", nodePositionx)
                    .attr("dy", nodePositiony)
                    .attr("text-anchor","middle")
                    .text(friend_data.name)
                    .attr("transform", function(d){return "translate(0,"+(userCircleRadius+20)+")"; });

