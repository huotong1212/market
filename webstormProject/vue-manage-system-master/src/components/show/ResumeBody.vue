<template>
    <div>
        <Header></Header>
        <el-container>
            <el-header></el-header>
            <el-main>
                <div class="main2">
                    <Best></Best>
                </div>
            </el-main>
            <el-footer></el-footer>
        </el-container>
        <Footer></Footer>
    </div>
</template>

<script>
    import ResumeHeader from './ResumeHeader'
    import ResumeFooter from "./ResumeFooter";
    import {getShowResume} from "../api/api";
    import {provinceAndCityData, REGION_DATA, CodeToText} from 'element-china-area-data'
    import left from './left-right-rtl'

    export default {
        name: "ResumeBody",
        data() {
            return {
                code: '',
                userResume: {
                    username: '',
                    mobile: '',
                    email: '',
                    gender: '',
                    birthday: '',
                },
                expectation: {
                    job: '',
                    province: '',
                    city: '',
                    salary_min: '',
                    salary_max: '',
                    duty_time: '',
                },
                options: provinceAndCityData,
                selectedOptions: [],
                dutyTimeChoice: {
                    1: '一个月内到岗',
                    2: '两个月内到岗',
                    3: '一周内到岗',
                },
                education: [],
                activeNames: ['1'],
                workExperience: [],
                projectExperience:[],
                tecnology: {
                    1: '前端',
                    3: '后端',
                    4: '数据库',
                    5: '语言',
                },
                texts: ['了解', '熟练', '精通', '大牛',],
                skills:[],
                textarea: '',
                appraise:{},
            }
        },
        computed: {
            classification() {
                return Object.keys(this.dutyTimeChoice)
            },
            data() {
                let data = new Map();
                this.skills.forEach(function (element, index) {
                    // console.log(element); // red green blue
                    // console.log(index);   // 0 1 2

                    // 转为int,因为在Set中的key最好为基础类型，2个不同的对象被认为是2个key
                    let category = Number.parseInt(element.category)

                    // 判断是否被添加过
                    if (!data.has(category)) {
                        data.set(category, [])
                    }

                    data.get(category).push(element)
                });
                return data
            },
        },
        components: {
            'Header': ResumeHeader,
            'Footer': ResumeFooter,
            'Best':left,
        },
        methods: {
            GetRequest() {
                //let url = window.location.search; //获取url中"?"符后的字串
                let url2 = window.location.href
                let index = url2.indexOf("?")
                if (index != -1) {  //判断是否有参数
                    let str = url2.substr(index + 1); //从第一个字符开始 因为第0个是?号 获取所有除问号的所有符串
                    this.code = str.split("=")[1];  //用等号进行分隔 （因为知道只有一个参数 所以直接用等号进分隔 如果有多个参数 要用&号分隔 再用等号进行分隔）
                    //console.log(this.code);     //直接弹出第一个参数 （如果有多个参数 还要进行循环的）
                }
            },
            getShowResume() {
                getShowResume(
                    {
                        code: this.code
                    }
                ).then((response) => {
                    //console.log('getShowResume', response)
                    this.setUserResume(response)
                    this.setExpectation(response)
                    this.education = response.data.education
                    this.workExperience = response.data.work
                    this.projectExperience = response.data.project
                    this.skills = response.data.skills
                    this.appraise = response.data.appraise
                }).catch(function (error) {

                })
            },
            setUserResume(response) {
                this.userResume.username = response.data.username
                this.userResume.mobile = response.data.mobile
                this.userResume.email = response.data.email
                this.userResume.gender = response.data.gender
                this.userResume.birthday = response.data.birthday
            },
            setExpectation(response) {
                this.expectation = response.data.expectation
                this.selectedOptions = [this.expectation.province, this.expectation.city]

            },
            dealChange(value) {
                //console.log(value)
                // code转汉字大对象
                this.expectation.province = value[0]
                this.expectation.city = value[1]
                // this.expectation.city = CodeToText[value[1]]
            },
        },
        mounted() {
            // this.GetRequest()
            // this.getShowResume()
        }
    }
</script>

<style lang="less" scoped>
    @import "../../assets/css/style.css";
</style>
