(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{26:function(e,t,a){e.exports=a(46)},31:function(e,t,a){},35:function(e,t,a){},38:function(e,t,a){},40:function(e,t,a){},44:function(e,t,a){},46:function(e,t,a){"use strict";a.r(t);var n=a(1),r=a.n(n),c=a(22),i=a.n(c),s=a(9),l=a(10),o=a(12),m=a(11),u=a(13),h=a(6),d=a(67),p=a(68),E=a(19),f=a.n(E),b=a(47),v=a(48),y=a(49),g=a(50),j=a(51),O=a(52),k=a(53),C=a(54),x=a(55),S=a(56),N=a(57),w=a(69),P=a(58),T=(a(31),function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).state={_id:a.props.match.params.id,customer:{},entities:[],intent:null,messages:[]},a.fetchChat=a.fetchChat.bind(Object(h.a)(Object(h.a)(a))),a.send=a.send.bind(Object(h.a)(Object(h.a)(a))),a.predict=a.predict.bind(Object(h.a)(Object(h.a)(a))),a}return Object(u.a)(t,e),Object(l.a)(t,[{key:"componentDidMount",value:function(){var e=this;this.timer=setInterval(function(){return e.fetchChat()},1e3)}},{key:"componentWillUnmount",value:function(){clearInterval(this.timer)}},{key:"fetchChat",value:function(){var e=this;return fetch("/api/chats/".concat(this.state._id),{method:"GET",credentials:"same-origin"}).then(function(t){return t.ok?t.json():{_id:e.state._id,customer:{},entities:[],intent:null,messages:[]}}).then(function(t){return e.setState({_id:t._id,customer:t.customer,entities:t.entities,intent:t.intent,messages:t.messages})})}},{key:"send",value:function(e){var t=this;return fetch("/api/chats/".concat(this.state._id,"/messages"),{method:"POST",credentials:"same-origin",body:JSON.stringify({text:e})}).then(function(e){e.ok&&t.setState({messages:t.state.messages.concat(e.json())})})}},{key:"predict",value:function(){var e=this;return fetch("/api/chats/".concat(this.state._id,"/predict"),{method:"POST",credentials:"same-origin"}).then(function(t){return t.ok?t.json():{entities:e.state.entities,intent:e.state.intent}}).then(function(t){return e.setState({entities:t.entities,intent:t.intent})})}},{key:"render",value:function(){return r.a.createElement("div",{className:"Chat"},r.a.createElement(b.a,null,r.a.createElement(v.a,null,r.a.createElement(y.a,{xs:"8"},r.a.createElement(_,{customer:this.state.customer,messages:this.state.messages})),r.a.createElement(y.a,{xs:{offset:1,size:3}},r.a.createElement(I,{entities:this.state.entities,intent:this.state.intent})))),r.a.createElement(K,{send:this.send,predict:this.predict}))}}]),t}(r.a.Component));function _(e){for(var t=[],a=0;a<e.messages.length;a++)t.push(r.a.createElement(D,{customer:e.customer,message:e.messages[a]}));return r.a.createElement("div",{className:"Messages"},t)}function D(e){return"customer"===e.message.sender?r.a.createElement("div",{className:"Message"},r.a.createElement(v.a,{className:"align-items-center h-100"},r.a.createElement(y.a,{xs:"4",className:"text-center"},r.a.createElement("strong",null,e.customer.first_name),r.a.createElement("br",null),r.a.createElement(f.a,{time:e.message.timestamp/1e3,format:"time"})),r.a.createElement(y.a,{xs:"8"},r.a.createElement(g.a,{body:!0,outline:!0,color:"primary"},r.a.createElement(j.a,null,e.message.text))))):r.a.createElement("div",{className:"Message"},r.a.createElement(v.a,{className:"align-items-center h-100"},r.a.createElement(y.a,{xs:"8"},r.a.createElement(g.a,{body:!0,outline:!0,color:"secondary"},r.a.createElement(j.a,null,e.message.text))),r.a.createElement(y.a,{xs:"4",className:"text-center"},r.a.createElement("strong",null,"You"),r.a.createElement("br",null),r.a.createElement(f.a,{time:e.message.timestamp/1e3,format:"time"}))))}function I(e){return r.a.createElement("div",{className:"Predictions"},null!==e.intent&&r.a.createElement(R,{intent:e.intent}),r.a.createElement(M,{entities:e.entities}))}function R(e){return r.a.createElement("div",{className:"Intent"},r.a.createElement("h2",null,"Intent"),r.a.createElement(O.a,null,r.a.createElement(k.a,null,e.intent)))}function M(e){for(var t=[],a=0;a<e.entities.length;a++)t.push(r.a.createElement(k.a,null,r.a.createElement(C.a,{color:"primary",pill:!0},e.entities[a].type),r.a.createElement("span",{className:"float-right"},'"',e.entities[a].snippet,'"')));return r.a.createElement("div",{className:"Entities"},r.a.createElement("h2",null,"Entities"),r.a.createElement(O.a,null,t))}var K=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).state={text:""},a.handleSendChange=a.handleSendChange.bind(Object(h.a)(Object(h.a)(a))),a.handleSendClick=a.handleSendClick.bind(Object(h.a)(Object(h.a)(a))),a.handleSendKeyPress=a.handleSendKeyPress.bind(Object(h.a)(Object(h.a)(a))),a.handlePredictClick=a.handlePredictClick.bind(Object(h.a)(Object(h.a)(a))),a}return Object(u.a)(t,e),Object(l.a)(t,[{key:"handleSendChange",value:function(e){e.preventDefault(),this.setState({text:e.target.value})}},{key:"handleSendClick",value:function(e){var t=this;e.preventDefault(),this.props.send(this.state.text).then(function(){return t.setState({text:""})})}},{key:"handleSendKeyPress",value:function(e){var t=this;"Enter"===e.key&&this.props.send(this.state.text).then(function(){return t.setState({text:""})})}},{key:"handlePredictClick",value:function(e){e.preventDefault(),this.props.predict()}},{key:"render",value:function(){return r.a.createElement("div",{className:"Footer"},r.a.createElement(x.a,{dark:!0,color:"primary",expand:"xs",fixed:"bottom"},r.a.createElement(b.a,null,r.a.createElement(S.a,{size:"lg",className:"mr-3"},r.a.createElement(N.a,{type:"text",value:this.state.text,onChange:this.handleSendChange,onKeyPress:this.handleSendKeyPress}),r.a.createElement(w.a,{addonType:"append"},r.a.createElement(P.a,{color:"success",onClick:this.handleSendClick},"Send"))),r.a.createElement(P.a,{color:"danger",size:"lg",onClick:this.handlePredictClick},"Predict"))))}}]),t}(r.a.Component),z=T,J=a(0),W=a.n(J),q=a(59),A=a(60),G=(a(35),function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).state={chats:[]},a.handleClick=a.handleClick.bind(Object(h.a)(Object(h.a)(a))),a}return Object(u.a)(t,e),Object(l.a)(t,[{key:"componentDidMount",value:function(){var e=this;this.timer=setInterval(function(){return e.fetchChats()},1e3)}},{key:"componentWillUnmount",value:function(){clearInterval(this.timer)}},{key:"fetchChats",value:function(){var e=this;fetch("/api/chats",{method:"GET",credentials:"same-origin"}).then(function(e){return e.ok?e.json():[]}).then(function(t){return e.setState({chats:t})})}},{key:"toRows",value:function(e){for(var t=[],a=0;a<e.length;a+=3){for(var n=[],c=a;c<e.length&&c<a+3;c++)n.push(this.toCol(e[c]));t.push(r.a.createElement(v.a,null,n))}return r.a.createElement("div",{className:"Rows"},t)}},{key:"toCol",value:function(e){var t=this;return r.a.createElement(y.a,{xs:"4"},r.a.createElement(g.a,null,r.a.createElement(q.a,null,r.a.createElement(A.a,{tag:"h2"},e.customer.full_name),r.a.createElement(j.a,null,e.message.text),r.a.createElement(P.a,{onClick:function(){return t.handleClick(e.message._id)},color:"success"},"Accept"))))}},{key:"handleClick",value:function(e){var t=this;fetch("/api/chats/".concat(e,"/employees"),{method:"POST",credentials:"same-origin"}).then(function(a){a.ok&&t.context.router.history.push("/chats/".concat(e))})}},{key:"render",value:function(){return r.a.createElement("div",{className:"Dashboard"},r.a.createElement(b.a,null,this.toRows(this.state.chats)))}}]),t}(r.a.Component));G.contextTypes={router:W.a.object.isRequired};var B=G,F=function(e){function t(){return Object(s.a)(this,t),Object(o.a)(this,Object(m.a)(t).apply(this,arguments))}return Object(u.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){var e=this.props.match;return r.a.createElement("div",{className:"Chats"},r.a.createElement(p.a,{path:e.path,exact:!0,component:B}),r.a.createElement(p.a,{path:"".concat(e.path,"/:id"),component:z}))}}]),t}(r.a.Component),H=a(61),U=a(62),L=a(63),Y=(a(38),function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).handleClick=a.handleClick.bind(Object(h.a)(Object(h.a)(a))),a}return Object(u.a)(t,e),Object(l.a)(t,[{key:"handleClick",value:function(e){var t=this;e.preventDefault(),this.props.logoutEmployee().then(function(){return t.context.router.history.push("/")})}},{key:"render",value:function(){return r.a.createElement("div",{className:"Header"},r.a.createElement(x.a,{dark:!0,color:"primary",expand:"xs"},r.a.createElement(b.a,null,r.a.createElement("h1",{className:"navbar-text"},"Contoso ACE"),null!==this.props.employee&&r.a.createElement(H.a,{navbar:!0},r.a.createElement(U.a,{className:"navbar-text mr-3"},"Hello, ",this.props.employee.first_name,"!"),r.a.createElement(U.a,null,r.a.createElement(L.a,{onClick:this.handleClick},"Sign Out"))))))}}]),t}(r.a.Component));Y.contextTypes={router:W.a.object.isRequired};var $=Y,Q=a(64),V=a(65),X=a(66),Z=(a(40),function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).handleSubmit=a.handleSubmit.bind(Object(h.a)(Object(h.a)(a))),a}return Object(u.a)(t,e),Object(l.a)(t,[{key:"handleSubmit",value:function(e){var t=this;e.preventDefault();var a=new FormData(e.target);this.props.loginEmployee(a.get("Email"),a.get("Password")).then(function(){return t.context.router.history.push("/chats")})}},{key:"render",value:function(){return r.a.createElement("div",{className:"Login"},r.a.createElement(b.a,null,r.a.createElement(v.a,null,r.a.createElement(y.a,{xs:{offset:3,size:6}},r.a.createElement(g.a,null,r.a.createElement(q.a,null,r.a.createElement(Q.a,{onSubmit:this.handleSubmit},r.a.createElement(V.a,null,r.a.createElement(X.a,{for:"Email"},"Email"),r.a.createElement(N.a,{type:"email",name:"Email",id:"Email",placeholder:"barbara@contoso.com"})),r.a.createElement(V.a,null,r.a.createElement(X.a,{for:"Password"},"Password"),r.a.createElement(N.a,{type:"password",name:"Password",id:"Password"})),r.a.createElement(P.a,{type:"submit",color:"primary"},"Sign In"))))))))}}]),t}(r.a.Component));Z.contextTypes={router:W.a.object.isRequired};var ee=Z,te=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(o.a)(this,Object(m.a)(t).call(this,e))).state={employee:null},a.loginEmployee=a.loginEmployee.bind(Object(h.a)(Object(h.a)(a))),a.logoutEmployee=a.logoutEmployee.bind(Object(h.a)(Object(h.a)(a))),a}return Object(u.a)(t,e),Object(l.a)(t,[{key:"componentDidMount",value:function(){this.fetchEmployee()}},{key:"fetchEmployee",value:function(){var e=this;return fetch("/api/employees/current",{method:"GET",credentials:"same-origin"}).then(function(e){return e.ok?e.json():null}).then(function(t){return e.setState({employee:t})})}},{key:"loginEmployee",value:function(e,t){var a=this;return fetch("/api/employees/login",{method:"POST",credentials:"same-origin",body:JSON.stringify({email:e,password:t})}).then(function(e){e.ok&&a.fetchEmployee()})}},{key:"logoutEmployee",value:function(){var e=this;return fetch("/api/employees/logout",{method:"POST",credentials:"same-origin"}).then(function(t){return t.ok?null:e.state.employee}).then(function(t){return e.setState({employee:t})})}},{key:"render",value:function(){var e=this;return r.a.createElement("div",{className:"App"},r.a.createElement(d.a,null,r.a.createElement("div",{className:"Router"},r.a.createElement($,{employee:this.state.employee,logoutEmployee:this.logoutEmployee}),r.a.createElement(p.a,{path:"/",exact:!0,render:function(t){return r.a.createElement(ee,Object.assign({},t,{loginEmployee:e.loginEmployee}))}}),r.a.createElement(p.a,{path:"/chats",component:F}))))}}]),t}(r.a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));a(42),a(44);i.a.render(r.a.createElement(te,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[26,2,1]]]);
//# sourceMappingURL=main.cabaa521.chunk.js.map