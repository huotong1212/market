<template>
    <div>
        <Header></Header>
        我是ResumeBody
        <Footer></Footer>
    </div>
</template>

<script>
    import ResumeHeader from './ResumeHeader'
    import ResumeFooter from "./ResumeFooter";
    import {getShowResume} from "../api/api";

    export default {
        name: "ResumeBody",
        data(){
            return{
                code:''
            }
        },
        components:{
            'Header':ResumeHeader,
            'Footer':ResumeFooter
        },
        methods:{
            GetRequest() {
                //let url = window.location.search; //获取url中"?"符后的字串
                let url2 = window.location.href
                let index = url2.indexOf("?")
                if (index != -1) {  //判断是否有参数
                    let str = url2.substr(index+1); //从第一个字符开始 因为第0个是?号 获取所有除问号的所有符串
                    this.code = str.split("=")[1];  //用等号进行分隔 （因为知道只有一个参数 所以直接用等号进分隔 如果有多个参数 要用&号分隔 再用等号进行分隔）
                    console.log(this.code);     //直接弹出第一个参数 （如果有多个参数 还要进行循环的）
                }
            },
            getShowResume(){
                getShowResume(
                    {
                        code:this.code
                    }
                ).then((response)=>{
                    console.log('getShowResume',response)
                }).catch(function (error) {

                })
            }
        },
        mounted() {
            this.GetRequest()
            this.getShowResume()
        }
    }
</script>

<style scoped>

</style>
