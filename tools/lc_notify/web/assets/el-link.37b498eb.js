import{b as k,aE as m,c,h as y,n as a,y as i,p as t,w as h,a9 as b,t as s,z as v,aa as o,s as r,D as d,_ as E,T as C}from"./index.74eb6c46.js";const g=k({type:{type:String,values:["primary","success","warning","info","danger","default"],default:"default"},underline:{type:Boolean,default:!0},disabled:{type:Boolean,default:!1},href:{type:String,default:""},icon:{type:m}}),w={click:l=>l instanceof MouseEvent},B=["href"],L=c({name:"ElLink"}),$=c({...L,props:g,emits:w,setup(l,{emit:u}){const p=l,n=y("link");function f(e){p.disabled||u("click",e)}return(e,S)=>(a(),i("a",{class:r([s(n).b(),s(n).m(e.type),s(n).is("disabled",e.disabled),s(n).is("underline",e.underline&&!e.disabled)]),href:e.disabled||!e.href?void 0:e.href,onClick:f},[e.icon?(a(),t(s(v),{key:0},{default:h(()=>[(a(),t(b(e.icon)))]),_:1})):o("v-if",!0),e.$slots.default?(a(),i("span",{key:1,class:r(s(n).e("inner"))},[d(e.$slots,"default")],2)):o("v-if",!0),e.$slots.icon?d(e.$slots,"icon",{key:2}):o("v-if",!0)],10,B))}});var P=E($,[["__file","/home/runner/work/element-plus/element-plus/packages/components/link/src/link.vue"]]);const z=C(P);export{z as E};
