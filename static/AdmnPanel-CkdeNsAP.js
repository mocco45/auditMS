import{o as r,c as v,a as e,r as d,u as $,b as L,d as S,e as C,f as i,w as u,g as f,n as A,h as w,t as j,i as U,j as b,k as M,l as p,v as x,m as D}from"./index-CsNuYJGr.js";import{u as E}from"./accessStore-Bqs8kJdE.js";function O(m,o){return r(),v("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24","stroke-width":"1.5",stroke:"currentColor","aria-hidden":"true","data-slot":"icon"},[e("path",{"stroke-linecap":"round","stroke-linejoin":"round",d:"m19.5 8.25-7.5 7.5-7.5-7.5"})])}function T(m,o){return r(),v("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24","stroke-width":"1.5",stroke:"currentColor","aria-hidden":"true","data-slot":"icon"},[e("path",{"stroke-linecap":"round","stroke-linejoin":"round",d:"m4.5 15.75 7.5-7.5 7.5 7.5"})])}function _(m){const n=m.trim().split(" ").filter(g=>g.length>0);return n.length>1?n[0][0].toUpperCase()+n[1][0].toUpperCase():n[0][0].toUpperCase()}const z={class:"flex h-screen"},F={class:"bg-gray-800 w-64 p-4"},I={class:"text-white py-2 hover:bg-gray-600"},R={class:"text-white py-2 hover:bg-gray-600"},q={class:"text-white py-2 hover:bg-gray-600"},G={class:"text-white py-2 hover:bg-gray-600"},H={class:"flex-1 flex flex-col"},J={class:"bg-gray-300 text-white p-4 flex justify-between items-center"},K={class:"flex items-center space-x-2"},Q={class:"relative"},W={key:0,ref:"dropdown",class:"w-24 h-20 px-4 py-4 bg-slate-700 absolute top-20 right-1"},X={class:"p-8 flex-1"},Y={key:0,class:"fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center"},Z={class:"bg-white p-8 rounded shadow-lg w-2/3 h-4/5"},ee={class:"flex justify-between"},te={action:""},se={class:"grid grid-cols-2"},le={class:"flex flex-col gap-y-4 mt-10 items-center w-full"},oe={class:"flex justify-start w-80 me-9"},ne={class:"flex justify-center mt-10 w-full"},re="chobja@gmail.com",ue={__name:"AdmnPanel",setup(m){const o=d(!1),n=d(!1),g=d(null),c=d(!1),y=d(!1);$(),E();const V=_("inocent john"),B=()=>{y.value?c.value=!0:c.value=!1},N=(()=>{const l=["#f87171","#60a5fa","#34d399","#facc15","#a78bfa"];return l[Math.floor(Math.random()*l.length)]})(),k=()=>{o.value=!1},h=l=>{g.value&&!g.value.contains(l.target)&&k()};return L(()=>{document.addEventListener("click",h)}),S(()=>{document.removeEventListener("click",h)}),(l,t)=>{const a=C("router-link"),P=C("router-view");return r(),v("div",z,[e("div",F,[t[14]||(t[14]=e("h2",{class:"text-white text-2xl mb-8"},"Sidebar",-1)),e("ul",null,[e("li",I,[i(a,{to:"/dashboard"},{default:u(()=>t[10]||(t[10]=[f("Dashboard")])),_:1})]),e("li",R,[i(a,{to:"/user-list"},{default:u(()=>t[11]||(t[11]=[f("User")])),_:1})]),e("li",q,[i(a,{to:""},{default:u(()=>t[12]||(t[12]=[f("Profile")])),_:1})]),e("li",G,[i(a,{to:""},{default:u(()=>t[13]||(t[13]=[f("Messages")])),_:1})])])]),e("div",H,[e("div",J,[t[16]||(t[16]=e("div",{class:"text-xl"},"Topbar",-1)),t[17]||(t[17]=e("div",null,[e("button",{class:"bg-blue-500 px-4 py-2 rounded"},"Login")],-1)),e("div",K,[e("div",{class:"w-10 h-10 rounded-full flex items-center justify-center text-white font-bold",style:A({backgroundColor:w(N)})},j(w(V)),5),e("p",{class:"text-gray-800"},j(re)),e("div",Q,[o.value?(r(),U(w(T),{key:0,onClick:t[0]||(t[0]=s=>o.value=!o.value),class:"w-4 text-black"})):b("",!0),o.value?b("",!0):(r(),U(w(O),{key:1,onClick:t[1]||(t[1]=s=>o.value=!o.value),class:"w-4 text-black"}))]),o.value?(r(),v("div",W,[e("ul",null,[e("li",null,[e("button",{onClick:t[2]||(t[2]=s=>{n.value=!0,k()}),class:"cursor-pointer"},"Profile")]),e("li",null,[i(a,{to:""},{default:u(()=>t[15]||(t[15]=[f("Logout")])),_:1})])])],512)):b("",!0)])]),e("div",X,[i(P),n.value?(r(),v("div",Y,[e("div",Z,[e("div",ee,[t[19]||(t[19]=e("h2",{class:"text-xl font-bold mb-4"},"Profile",-1)),e("button",{onClick:t[3]||(t[3]=s=>n.value=!1),class:"mb-4"},t[18]||(t[18]=[e("svg",{xmlns:"http://www.w3.org/2000/svg",class:"h-6 w-6 text-gray-500 hover:text-gray-700",fill:"none",viewBox:"0 0 24 24",stroke:"currentColor"},[e("path",{"stroke-linecap":"round","stroke-linejoin":"round","stroke-width":"2",d:"M6 18L18 6M6 6l12 12"})],-1)]))]),e("form",te,[e("div",se,[t[25]||(t[25]=e("div",{class:"flex justify-end"},[e("div",{class:"w-96 h-96 bg-slate-600 rounded-full"})],-1)),e("div",le,[e("div",{class:M([c.value?"":"mt-24","w-4/5","space-y-3"])},[e("div",null,[t[20]||(t[20]=e("label",{for:"full",class:"block text-sm font-medium text-gray-700"},"Full Name",-1)),p(e("input",{"onUpdate:modelValue":t[4]||(t[4]=s=>l.full=s),id:"full",class:"rounded-full w-full border border-gray-400 px-3 py-2 shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500",type:"text"},null,512),[[x,l.full]])]),e("div",null,[t[21]||(t[21]=e("label",{for:"email",class:"block text-sm font-medium text-gray-700"},"Email",-1)),p(e("input",{"onUpdate:modelValue":t[5]||(t[5]=s=>l.emaili=s),id:"email",class:"rounded-full w-full border border-gray-400 px-3 py-2 shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500",type:"email"},null,512),[[x,l.emaili]])])],2),e("div",{class:M([c.value?"":"hidden","w-4/5","space-y-3"])},[e("div",null,[t[22]||(t[22]=e("label",{for:"old",class:"block text-sm font-medium text-gray-700"},"Old Password",-1)),p(e("input",{"onUpdate:modelValue":t[6]||(t[6]=s=>l.password=s),id:"old",class:"rounded-full w-full border border-gray-400 px-3 py-2 shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500",type:"password"},null,512),[[x,l.password]])]),e("div",null,[t[23]||(t[23]=e("label",{for:"pass",class:"block text-sm font-medium text-gray-700"},"New Password",-1)),p(e("input",{"onUpdate:modelValue":t[7]||(t[7]=s=>l.password=s),id:"pass",class:"rounded-full w-full border border-gray-400 px-3 py-2 shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500",type:"password"},null,512),[[x,l.password]])])],2),e("div",oe,[p(e("input",{type:"checkbox","onUpdate:modelValue":t[8]||(t[8]=s=>y.value=s),onChange:B},null,544),[[D,y.value]]),t[24]||(t[24]=e("span",{class:"ms-2"},"reset password",-1))])])])]),e("div",ne,[e("button",{onClick:t[9]||(t[9]=s=>n.value=!1),class:"bg-blue-900 hover:bg-blue-700 text-white px-4 py-2 rounded"}," update ")])])])):b("",!0)])])])}}};export{ue as default};