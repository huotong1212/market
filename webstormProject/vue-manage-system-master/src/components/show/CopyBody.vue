<template>
    <div>
        <Header></Header>
        我是ResumeBody


        <el-container>
            <el-header>Header</el-header>
            <el-main>
                <div class="main2">
<!--                    &lt;!&ndash;基本信息&ndash;&gt;-->
<!--                    <el-card class="box-card box-card-left" shadow="hover">-->
<!--                        <div slot="header" class="clearfix">-->
<!--                            <span class="text">基本信息</span>-->
<!--                            &lt;!&ndash;                <el-button style="float: right; padding: 3px 0" type="text" @click="updateUserResume('userResume')">保存</el-button>&ndash;&gt;-->
<!--                        </div>-->

<!--                        &lt;!&ndash;UserResume表单&ndash;&gt;-->
<!--                        <div class="form-box align-center">-->
<!--                            <el-form ref="userResume" :model="userResume" label-width="80px">-->
<!--                                <el-form-item label="姓名" prop="username">-->
<!--                                    <el-input v-model="userResume.username"></el-input>-->
<!--                                </el-form-item>-->
<!--                                <el-form-item label="性别" prop="gender">-->
<!--                                    <el-radio-group v-model="userResume.gender">-->
<!--                                        <el-radio label="male">男</el-radio>-->
<!--                                        <el-radio label="female">女</el-radio>-->
<!--                                    </el-radio-group>-->
<!--                                </el-form-item>-->
<!--                                <el-form-item label="出身日期" prop="birthday">-->
<!--                                    <el-col :span="11">-->
<!--                                        <el-date-picker value-format="yyyy-MM-dd" type="date" placeholder="选择日期"-->
<!--                                                        v-model="userResume.birthday"-->
<!--                                                        style="width: 100%;"></el-date-picker>-->
<!--                                    </el-col>-->
<!--                                </el-form-item>-->

<!--                                <el-form-item label="邮箱" prop="email">-->
<!--                                    <el-input v-model="userResume.email"></el-input>-->
<!--                                </el-form-item>-->

<!--                                <el-form-item label="手机号" prop="mobile">-->
<!--                                    <el-input v-model="userResume.mobile"></el-input>-->
<!--                                </el-form-item>-->
<!--                            </el-form>-->
<!--                        </div>-->
<!--                    </el-card>-->

<!--                    &lt;!&ndash;求职意向&ndash;&gt;-->
<!--                    <el-card class="box-card box-card-left" shadow="hover">-->
<!--                        <div slot="header" class="clearfix">-->
<!--                            <span class="text">求职意向</span>-->
<!--                        </div>-->

<!--                        &lt;!&ndash;Expectation&ndash;&gt;-->
<!--                        <div class="form-box align-center">-->
<!--                            <el-form ref="expectation" :model="expectation" label-width="80px">-->
<!--                                <el-form-item label="岗位" prop="job">-->
<!--                                    <el-input v-model="expectation.job"></el-input>-->
<!--                                </el-form-item>-->
<!--                                <el-form-item label="城市" prop="city">-->
<!--                                    <el-cascader-->
<!--                                            size="large"-->
<!--                                            :options="options"-->
<!--                                            v-model="selectedOptions"-->
<!--                                            @change="dealChange">-->
<!--                                    </el-cascader>-->
<!--                                </el-form-item>-->

<!--                                <el-form-item label="到岗时间" prop="duty_time">-->
<!--                                    <el-select v-model="expectation.duty_time" placeholder="请选择到岗时间">-->
<!--                                        <el-option v-for="index in classification" :key="Number(index)"-->
<!--                                                   :label="dutyTimeChoice[index]" :value="Number(index)"></el-option>-->
<!--                                    </el-select>-->
<!--                                </el-form-item>-->

<!--                                <el-form-item label="薪资范围" prop="salary_min">-->
<!--                                    <el-col :span="10"> 最低（K）：-->
<!--                                        <el-input-number v-model="expectation.salary_min" controls-position="right"-->
<!--                                                         :min="1" :max="100">-->

<!--                                        </el-input-number>-->
<!--                                    </el-col>-->
<!--                                    <el-col class="line" :span="1">-</el-col>-->
<!--                                    <el-col :span="11"> 最高（K）：-->
<!--                                        <el-input-number v-model="expectation.salary_max" controls-position="right"-->
<!--                                                         :min="1" :max="100">-->
<!--                                        </el-input-number>-->
<!--                                    </el-col>-->
<!--                                    &emsp;&emsp;-->
<!--                                </el-form-item>-->

<!--                            </el-form>-->
<!--                        </div>-->
<!--                    </el-card>-->

<!--                    &lt;!&ndash;教育背景&ndash;&gt;-->
<!--                    <el-card class="box-card box-card-left" shadow="hover">-->
<!--                        <div slot="header" class="clearfix">-->
<!--                            <span class="text">教育背景</span>-->
<!--                        </div>-->

<!--                        &lt;!&ndash;允许多个教育背景&ndash;&gt;-->
<!--                        <el-collapse v-model="activeNames">-->

<!--                            <el-collapse-item v-for="item in education" :key="item.id" :name="item.graduate_school">-->
<!--                                <template slot="title">-->
<!--                                    <span style="width: 90%">-->
<!--                                        <i class="header-icon el-icon-arrow-right"></i><span-->
<!--                                            class="tform">{{item.graduate_school}}</span>-->
<!--                                    </span>-->
<!--                                </template>-->

<!--                                &lt;!&ndash;Education&ndash;&gt;-->
<!--                                <div class="form-box">-->
<!--                                    <el-form ref="form" :model="item" label-width="80px">-->
<!--                                        <el-form-item label="时期" prop="enrollment_date">-->
<!--                                            <el-col :span="11">-->
<!--                                                <el-date-picker value-format="yyyy-MM-dd" @change="dateChange(item.id)"-->
<!--                                                                type="date" placeholder="入学日期"-->
<!--                                                                v-model="item.enrollment_date"-->
<!--                                                                style="width: 100%;"></el-date-picker>-->
<!--                                            </el-col>-->
<!--                                            <el-col class="line" :span="2">-</el-col>-->
<!--                                            <el-col :span="11">-->
<!--                                                <el-date-picker value-format="yyyy-MM-dd" @change="dateChange(item.id)"-->
<!--                                                                placeholder="毕业日期" v-model="item.graduate_date"-->
<!--                                                                style="width: 100%;"></el-date-picker>-->
<!--                                            </el-col>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="毕业院校" prop="graduate_school">-->
<!--                                            <el-input maxlength="20" v-model="item.graduate_school"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="课程描述" prop="subjects">-->
<!--                                            <el-input maxlength="100" v-model="item.subjects"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="突出表现" prop="emphasize">-->
<!--                                            <el-input maxlength="100" type="textarea" rows="3"-->
<!--                                                      v-model="item.emphasize"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                    </el-form>-->
<!--                                </div>-->
<!--                            </el-collapse-item>-->
<!--                        </el-collapse>-->
<!--                    </el-card>-->

<!--                    &lt;!&ndash;工作经验&ndash;&gt;-->
<!--                    <el-card class="box-card box-card-left" shadow="hover">-->
<!--                        <div slot="header" class="clearfix">-->
<!--                            <span class="text">工作经验</span>-->
<!--                        </div>-->

<!--                        &lt;!&ndash;允许多个工作经验&ndash;&gt;-->
<!--                        &lt;!&ndash;允许多个工作经验&ndash;&gt;-->
<!--                        <el-collapse v-model="activeNames">-->

<!--                            <el-collapse-item v-for="item in workExperience" :key="item.id" name="item.id">-->
<!--                                <template slot="title">-->
<!--                                    <span style="width: 90%">-->
<!--                                        <i class="header-icon el-icon-arrow-right"></i><span class="tform">{{item.company}}</span>-->
<!--                                    </span>-->
<!--                                </template>-->

<!--                                &lt;!&ndash;WorkExperience&ndash;&gt;-->
<!--                                <div class="form-box">-->
<!--                                    <el-form ref="item" :model="item" label-width="80px">-->
<!--                                        <el-form-item label="企业名称" prop="company">-->
<!--                                            <el-input maxlength="20" v-model="item.company"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="时期">-->
<!--                                            <el-col :span="11">-->
<!--                                                <el-date-picker value-format="yyyy-MM-dd"-->
<!--                                                                type="date" placeholder="开始时间" v-model="item.start_time"-->
<!--                                                                style="width: 100%;"></el-date-picker>-->
<!--                                            </el-col>-->
<!--                                            <el-col class="line" :span="2">-</el-col>-->
<!--                                            <el-col :span="11">-->
<!--                                                <el-date-picker value-format="yyyy-MM-dd"-->
<!--                                                                placeholder="结束时间" v-model="item.end_time"-->
<!--                                                                style="width: 100%;"></el-date-picker>-->
<!--                                            </el-col>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="任职部门" prop="department">-->
<!--                                            <el-input maxlength="100" v-model="item.department"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="任职岗位" prop="profession">-->
<!--                                            <el-input maxlength="100" v-model="item.profession"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="岗位职责" prop="duty">-->
<!--                                            <el-input maxlength="100" type="textarea" rows="3"-->
<!--                                                      v-model="item.duty"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                    </el-form>-->
<!--                                </div>-->
<!--                            </el-collapse-item>-->
<!--                        </el-collapse>-->
<!--                    </el-card>-->

<!--                    &lt;!&ndash;项目经验&ndash;&gt;-->
<!--                    <el-card class="box-card box-card-left" shadow="hover">-->
<!--                        <div slot="header" class="clearfix">-->
<!--                            <span class="text">项目经验</span>-->
<!--                        </div>-->
<!--                        &lt;!&ndash;允许多个项目经验&ndash;&gt;-->
<!--                        <el-collapse>-->

<!--                            <el-collapse-item v-for="item in projectExperience" :key="item.id" name="item.id">-->
<!--                                <template slot="title">-->
<!--                                    <span style="width: 90%">-->
<!--                                        <i class="header-icon el-icon-arrow-right"></i><span class="tform">{{item.project_name}}</span>-->
<!--                                     </span>-->
<!--                                </template>-->

<!--                                &lt;!&ndash;Project&ndash;&gt;-->
<!--                                <div class="form-box">-->
<!--                                    <el-form ref="item"  :model="item" label-width="80px">-->
<!--                                        <el-form-item label="时期">-->
<!--                                            <el-col :span="11">-->
<!--                                                <el-date-picker value-format="yyyy-MM-dd" type="date" placeholder="开始时间"-->
<!--                                                                v-model="item.start_time"-->
<!--                                                                style="width: 100%;"></el-date-picker>-->
<!--                                            </el-col>-->
<!--                                            <el-col class="line" :span="2">-</el-col>-->
<!--                                            <el-col :span="11">-->
<!--                                                <el-date-picker value-format="yyyy-MM-dd" placeholder="结束时间"-->
<!--                                                                v-model="item.end_time"-->
<!--                                                                style="width: 100%;"></el-date-picker>-->
<!--                                            </el-col>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="项目名称" prop="project_name">-->
<!--                                            <el-input maxlength="30" v-model="item.project_name"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="技术使用" prop="project_skills">-->
<!--                                            <el-input maxlength="100" v-model="item.project_skills"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="项目职责" prop="tasks">-->
<!--                                            <el-input maxlength="1000" type="textarea" rows="3"-->
<!--                                                      v-model="item.tasks"></el-input>-->
<!--                                        </el-form-item>-->
<!--                                    </el-form>-->
<!--                                </div>-->
<!--                            </el-collapse-item>-->
<!--                        </el-collapse>-->
<!--                    </el-card>-->

<!--                    &lt;!&ndash;技能特长&ndash;&gt;-->
<!--                    <el-card class="box-card box-card-left" shadow="hover">-->
<!--                        <div slot="header" class="clearfix">-->
<!--                            <span class="text">技能特长</span>-->
<!--                        </div>-->

<!--                        &lt;!&ndash;允许多个技能特长&ndash;&gt;-->
<!--                        &lt;!&ndash;允许多个技能&ndash;&gt;-->
<!--                        <el-collapse >-->

<!--                            <el-collapse-item v-for="[key,item] in data" :key="key" name="key">-->
<!--                                <template slot="title">-->
<!--                                    <span style="width: 95%">-->
<!--                                        <i class="header-icon el-icon-arrow-right"></i><span class="tform">{{tecnology[key]}}</span>-->
<!--                                    </span>-->
<!--                                </template>-->

<!--                                &lt;!&ndash;Skills&ndash;&gt;-->
<!--                                <div class="e-rate" v-for="skill of item">-->
<!--                                    <el-input :disabled="true" placeholder="请输入内容" v-model="skill.skill_desc" style="width: 70%">-->
<!--                                        <template slot="prepend">{{skill.skill_tag}}</template>-->
<!--                                    </el-input>-->
<!--                                    &emsp;&emsp;&emsp;-->
<!--                                    <el-rate :disabled="true" class="e-rate" v-model="skill.skill_level" show-text :max=4-->
<!--                                             :texts="texts">-->
<!--                                    </el-rate>-->
<!--                                    &ensp;&ensp;&ensp;&ensp;-->
<!--                                </div>-->
<!--                            </el-collapse-item>-->
<!--                        </el-collapse>-->
<!--                    </el-card>-->

<!--                    &lt;!&ndash;自我评价&ndash;&gt;-->
<!--                    <el-card class="box-card box-card-left" shadow="hover">-->
<!--                        <div slot="header" class="clearfix">-->
<!--                            <span class="text">自我评价</span>-->
<!--                        </div>-->

<!--                        &lt;!&ndash;自我评价只有一个&ndash;&gt;-->
<!--                        <el-input-->
<!--                                type="textarea"-->
<!--                                :autosize="{ minRows: 3, maxRows: 10}"-->
<!--                                placeholder="请输入内容"-->
<!--                                maxlength="500"-->
<!--                                v-model="appraise.self_desc">-->
<!--                        </el-input>-->
<!--                    </el-card>-->
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
                    console.log(this.code);     //直接弹出第一个参数 （如果有多个参数 还要进行循环的）
                }
            },
            getShowResume() {
                getShowResume(
                    {
                        code: this.code
                    }
                ).then((response) => {
                    console.log('getShowResume', response)
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
                console.log(value)
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
