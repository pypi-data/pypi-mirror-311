import{r as a,j as e}from"./@radix-DeK6qiuw.js";import{S as p}from"./trash-arLUMWMS.js";import{u as j,D as x,a as D}from"./delete-run-CJdh1P_h.js";import{i as R,t as C,v as w,f as b,D as y,w as S,x as v,C as A}from"./index-CCOPpudF.js";import{S as O}from"./dots-horizontal-otGBOSDJ.js";import{A as k}from"./AlertDialogDropdownItem-DezXKmDf.js";import{c as T}from"./@tanstack-DT5WLu9C.js";const g=a.createContext(null);function z({children:t}){const[s,r]=a.useState([]),l=T(),{toast:n}=R(),u=j(),o=async i=>{try{const c=i.map(f=>u.mutateAsync({runId:f}));await Promise.all(c),n({description:"Deleted successfully.",status:"success",emphasis:"subtle",rounded:!0}),await l.invalidateQueries({queryKey:["runs"]}),r([])}catch(c){console.error("Failed to delete some runs:",c)}};return e.jsx(g.Provider,{value:{selectedRuns:s,setSelectedRuns:r,bulkDeleteRuns:o},children:t})}function h(){const t=a.useContext(g);if(!t)throw new Error("useRunsSelectorContext must be used within a RunsSelectorProvider");return t}function N(){const[t,s]=a.useState(!1),{bulkDeleteRuns:r,selectedRuns:l}=h();async function n(){await r(l),s(!1)}return e.jsxs(C,{open:t,onOpenChange:s,children:[e.jsx(w,{children:e.jsxs(b,{className:"rounded-sharp border-none bg-white",size:"md",emphasis:"subtle",intent:"secondary",children:[e.jsx(p,{className:"h-5 w-5 shrink-0 gap-1 fill-neutral-400"}),"Delete"]})}),e.jsx(x,{title:`Delete Run${l.length>=2?"s":""}`,handleDelete:n,children:e.jsxs(D,{children:[e.jsx("p",{children:"Are you sure?"}),e.jsx("p",{children:"This action cannot be undone."})]})})]})}function F(){const{selectedRuns:t}=h();return e.jsxs("div",{className:"flex items-center divide-x divide-theme-border-moderate overflow-hidden rounded-md border border-theme-border-moderate",children:[e.jsx("div",{className:"bg-primary-25 px-2 py-1 font-semibold text-theme-text-brand",children:`${t==null?void 0:t.length} Run${(t==null?void 0:t.length)>1?"s":""} selected`}),e.jsx(N,{})]})}function H({id:t}){const[s,r]=a.useState(!1),[l,n]=a.useState(!1),u=a.useRef(null),o=a.useRef(null),{bulkDeleteRuns:i}=h();async function c(){await i([t]),m(!1)}function f(){o.current=u.current}function m(d){if(d===!1){n(!1),setTimeout(()=>{r(d)},200);return}r(d)}return e.jsxs(y,{onOpenChange:n,open:l,children:[e.jsx(S,{ref:u,children:e.jsx(O,{className:"h-4 w-4 fill-theme-text-tertiary"})}),e.jsx(v,{hidden:s,onCloseAutoFocus:d=>{o.current&&(o.current.focus(),o.current=null,d.preventDefault())},align:"end",sideOffset:7,children:e.jsx(k,{onSelect:f,open:s,onOpenChange:m,triggerChildren:"Delete",icon:e.jsx(p,{fill:"red"}),children:e.jsx(x,{title:"Delete Run",handleDelete:c,children:e.jsxs(D,{children:[e.jsx("p",{children:"Are you sure?"}),e.jsx("p",{children:"This action cannot be undone."})]})})})})]})}const Q=({id:t})=>{const{selectedRuns:s,setSelectedRuns:r}=h(),l=(n,u)=>{r(o=>n?[...o,u]:o.filter(i=>i!==u))};return e.jsx(A,{id:t,onCheckedChange:n=>l(n,t),checked:s.includes(t),className:"h-3 w-3"})};export{z as R,Q as a,H as b,F as c,h as u};
