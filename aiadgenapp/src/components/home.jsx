import { useState,useEffect } from 'react'
import axios from 'axios'
import Output from './output'

export default function Home() {
    const [formdata,setformdata]=useState({
      product_name:"",
      description:"",
      audience:"students",
      platform:"instagram",
      tone:"",
      duration:0,
    })
    const [adid,setadid]=useState(0)
    const fields=[
      {name:"product_name",label:"Product",type:"text"},
      {name:"description",label:"Description",type:"text"},
      {name:"audience",label:"Audience",type:"text"},
      {name:"platform",label:"Platform",type:"text"},
      {name:"tone",label:"Tone",type:"text"},
      {name:"duration",label:"Duration",type:"number"},
    ]
    const baseurl="http://127.0.0.1:8000/"
    useEffect(()=>{
      if(adid!==0){
        try{
          const interval=setInterval(async() => {
              const instance=await axios.get(`${baseurl}api/retrieve/${adid}`)
              if(instance.data.status==="pending"){
                console.log("task is pending")
              }
              else if(instance.data.status==="failed"){
                console.log("task failed")
                clearInterval(interval)
              }
              else{
                console.log("task is completed")
                clearInterval(interval)
              }
              return (()=>clearInterval(interval))
        }, 2000);
      }catch{
        console.log("an error occured")
      }
    }else{
      console.log("Input details")
    }
    },[adid])
    const handlesubmit=async(e)=>{
        e.preventDefault()
        if(formdata.product_name && formdata.description && formdata.audience && formdata.platform && formdata.tone && formdata.duration!=""){
          const apidata=await axios.post(`${baseurl}api/adgen/`,{
            product_name:formdata.product_name,
            description:formdata.description,
            audience:formdata.audience,
            platform:formdata.platform,
            tone:formdata.tone,
            duration:formdata.duration
          })
          console.log(apidata.data)
          setadid(apidata.data.id)
          alert("Your request has been submitted!")
        }else{
          alert("input missing")
        }
    }
    const handlechange=(e)=>{
      const {name,value}=e.target
      setformdata((prev)=>({...prev,[name]:name==="duration"?Number(value):value})) //js computed property
    }
  return (
    <div>
        <div className='flex flex-col items-start ml-4'>
        {fields.map((field)=>(
          <div>
          {
          field.name==="audience"?
          <div>
            <a>{field.label}</a><br/>
            <select name={field.name} value={formdata[field.name]} onChange={handlechange}>
              <option value="students">students</option>
              <option value="business">business</option>
              <option value="professional">professional</option>
            </select>
          </div>:
            field.name==="platform"?
            <div>
            <a>{field.label}</a><br/>
            <select name={field.name} value={formdata[field.name]} onChange={handlechange}>
              <option value="instagram">instagram</option>
              <option value="ytshorts">ytshorts</option>
              <option value="tiktok">tiktok</option>
            </select>
            </div>:
            <div><a>{field.label}</a><input type={field.type} name={field.name} value={formdata[field.name]} onChange={handlechange}/></div>
          }
          </div>
        ))}
        <button className='bg-blue-500 p-2 rounded-lg text-white active:bg-blue-700' type="submit" onClick={handlesubmit} >Submit</button>        </div>
    </div>
  )
}
