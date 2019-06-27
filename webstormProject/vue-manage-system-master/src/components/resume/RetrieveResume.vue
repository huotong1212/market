<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 表单</el-breadcrumb-item>
                <el-breadcrumb-item>创建简历</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">

            <!--基本信息-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">基本信息</span>
                    <el-button style="float: right; padding: 3px 0" type="text" @click="updateUserResume('userResume')">保存</el-button>
                </div>

                <!--UserResume表单-->
                <div class="form-box align-center">
                    <el-form ref="userResume" status-icon :rules="userResumeRules" :model="userResume" label-width="80px">
                        <el-form-item label="头像">
                            <div style="width: 50%">
                                <div class="crop-demo" style="display: inline-block">
                                    <img :src="cropImg" class="pre-img">
                                    <div class="crop-demo-btn" style="display: inline-block">选择图片
                                        <input class="crop-input" type="file" name="image" accept="image/*"
                                               @change="setImage"/>
                                    </div>
                                </div>

                                <el-dialog title="裁剪图片" :visible.sync="dialogVisible" width="30%">
                                    <vue-cropper ref='cropper' :src="imgSrc" :ready="cropImage" :zoom="cropImage"
                                                 :cropmove="cropImage"
                                                 style="width:100%;height:300px;"></vue-cropper>
                                    <span slot="footer" class="dialog-footer">
                                            <el-button @click="cancelCrop">取 消</el-button>
                                            <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
                                        </span>
                                </el-dialog>
                            </div>
                        </el-form-item>

                        <el-form-item label="姓名" prop="username">
                            <el-input v-model="userResume.username" ></el-input>
                        </el-form-item>
                        <el-form-item label="性别" prop="gender">
                            <el-radio-group v-model="userResume.gender">
                                <el-radio label="male">男</el-radio>
                                <el-radio label="female">女</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="出身日期" prop="birthday">
                            <el-col :span="11">
                                <el-date-picker value-format="yyyy-MM-dd" type="date" placeholder="选择日期"
                                                v-model="userResume.birthday" style="width: 100%;"></el-date-picker>
                            </el-col>
                        </el-form-item>

                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="userResume.email"></el-input>
                        </el-form-item>

                        <el-form-item label="手机号" prop="mobile">
                            <el-input v-model="userResume.mobile"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-card>

            <!--求职意向-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">求职意向</span>
                    <el-button @click="createOrUpdateExpect('expectation')" style="float: right; padding: 3px 0" type="text">保存</el-button>
                </div>

                <!--Expectation-->
                <div class="form-box align-center">
                    <el-form ref="expectation" status-icon :rules="expectationRules" :model="expectation" label-width="80px">
                        <el-form-item label="岗位" prop="job">
                            <el-input v-model="expectation.job"></el-input>
                        </el-form-item>
                        <el-form-item label="城市" prop="city">
                            <el-cascader
                                    size="large"
                                    :options="options"
                                    v-model="selectedOptions"
                                    @change="dealChange">
                            </el-cascader>
                        </el-form-item>

                        <el-form-item label="到岗时间" prop="duty_time">
                            <el-select v-model="expectation.duty_time" placeholder="请选择到岗时间">
                                <el-option v-for="index in classification" :key="Number(index)" :label="dutyTimeChoice[index]" :value="Number(index)"></el-option>
                            </el-select>
                        </el-form-item>

                        <el-form-item label="薪资范围" prop="salary_min">
                            <el-col :span="10"> 最低（K）：
                                <el-input-number v-model="expectation.salary_min" controls-position="right" @change="handleChange"
                                                 :min="1" :max="100">

                                </el-input-number>
                            </el-col>
                            <el-col class="line" :span="1">-</el-col>
                            <el-col :span="11"> 最高（K）：
                                <el-input-number v-model="expectation.salary_max" controls-position="right" @change="handleChange"
                                                 :min="1" :max="100">
                                </el-input-number>
                            </el-col>
                            &emsp;&emsp;
                            <span v-show="errorVisible" style="font-size: small;color: #f02d2d">{{error}}</span>
                        </el-form-item>

                    </el-form>
                </div>
            </el-card>

            <!--教育背景-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">教育背景</span>
                    <el-button @click="createEdu" style="float: right; padding: 3px 0" type="text">新增</el-button>
                    <el-button @click="saveEdu" style="float: right; padding: 3px 0" type="text">保存</el-button>
                </div>

                <!--允许多个教育背景-->
                <Education ref="edu" ></Education>
            </el-card>

            <!--工作经验-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">工作经验</span>
                    <el-button @click="createWork" style="float: right; padding: 3px 0" type="text">新增</el-button>
                    <el-button @click="saveWork" style="float: right; padding: 3px 0" type="text">保存</el-button>
                </div>

                <!--允许多个工作经验-->
                <WorkExperience ref="work"></WorkExperience>
            </el-card>

            <!--项目经验-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">项目经验</span>
                    <el-button @click="createProject" style="float: right; padding: 3px 0" type="text">新增</el-button>
                    <el-button @click="saveProject" style="float: right; padding: 3px 0" type="text">保存</el-button>                </div>

                <!--允许多个项目经验-->
                <ProjectExperience ref="project"></ProjectExperience>
            </el-card>

            <!--技能特长-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">技能特长</span>
                    <el-button @click="createSkill" style="float: right; padding: 3px 0" type="text">添加</el-button>
                </div>

                <!--允许多个技能特长-->
                <Skills ref="skill"></Skills>
            </el-card>

            <!--自我评价-->
            <el-card class="box-card box-card-left" shadow="hover">
                <div slot="header" class="clearfix">
                    <span class="text">自我评价</span>
                    <el-button @click="updateSelfAppraise" style="float: right; padding: 3px 0" type="text">保存</el-button>
                </div>

                <!--自我评价只有一个-->
                <el-input
                        type="textarea"
                        :autosize="{ minRows: 1, maxRows: 10}"
                        placeholder="请输入内容"
                        maxlength="500"
                        v-model="textarea">
                </el-input>
            </el-card>

            <!-- 编辑弹出框 -->


            <!--一键保存-->

            <el-button type="primary" style="margin-left: 10px" icon="el-icon-check" class="handle-create" @click="saveAll">保存所有</el-button>
            &emsp;&emsp;&emsp;&emsp;
            <el-button icon="el-icon-back" style="margin-right: 20px" class="handle-create" @click="back">返回</el-button>

            <!--UserResume表单-->

        </div>

    </div>
</template>

<script>
    import Education from "./Education";
    import WorkExperience from "./WorkExperience";
    import ProjectExperience from "./ProjectExperience";
    import Skills from "./Skills";
    import SelfAppraise from "./SelfAppraise";
    import customValidate from "../utils/customValidate";
    import cookie from "../static/cookie";
    import {
        getExpectation,
        getUserResume,
        updateUserResume,
        updateExpectation,
        createExpectation,
        getSelfAppraise, updateSelfAppraise
    } from "../api/api";
    import { provinceAndCityData,REGION_DATA,CodeToText } from 'element-china-area-data'
    import VueCropper from 'vue-cropperjs';


    export default {
        name: 'createResume',
        data: function () {
            return {
                resumeId: '',
                errorVisible:false,
                error:'',
                editVisible: false,
                textarea: '',
                options: provinceAndCityData,
                selectedOptions: [],
                userResume: {
                    username: '',
                    mobile: '',
                    email: '',
                    gender: '',
                    birthday: '',
                    portrait:'',
                },
                userResumeRules: {
                    username: [
                        {required: true, message: '请输入姓名', trigger: 'blur'},
                        {min: 2, max: 8, message: '长度在 2 到 8 个字符'}
                    ],
                    mobile: [
                        {required: true, message: '请输入手机号码', trigger: 'blur'},
                        {validator: customValidate.isMobile, trigger: 'blur'}
                    ],
                    email: [
                        {required: true, message: '请输入邮箱地址', trigger: 'blur'},
                        {validator: customValidate.isEmail, trigger: 'blur'}
                    ],
                    gender: [
                        {required: true, message: '请选择性别', trigger: 'blur'},
                    ],
                    birthday: [
                        {required: true, message: '请输入出生年月', trigger: 'blur'},
                    ],
                },
                activeNames: ['1'],
                expectationRules:{
                    job: [
                        {required: true, message: '请输入姓名', trigger: 'blur'},
                    ],
                    salary_min:[
                        {validator: customValidate.isInteger, trigger: 'blur'}
                    ],
                    salary_max:[
                        {validator: customValidate.isInteger, trigger: 'blur'}
                    ],
                },
                expectation:{
                    job:'',
                    province:'',
                    city:'',
                    salary_min:'',
                    salary_max:'',
                    duty_time:'',
                },
                createFlag:false,
                dutyTimeChoice: {
                    1: '一个月内到岗',
                    2: '两个月内到岗',
                    3: '一周内到岗',
                },
                //defaultSrc: require('../../assets/img/img.jpg'),
                defaultSrc: '',
                fileList: [],
                imgSrc: '',
                cropImg: '',
                dialogVisible: false,
                file:'',
            }
        },
        methods: {
            onSubmit() {
                this.$message.success('提交成功！');
            },
            // 保存编辑
            saveEdit() {
                this.editVisible = false;
                this.$message.success(`修改第 ${this.idx + 1} 行成功`);
                if (this.tableData[this.idx].id === this.id) {
                    this.$set(this.tableData, this.idx, this.form);
                } else {
                    for (let i = 0; i < this.tableData.length; i++) {
                        if (this.tableData[i].id === this.id) {
                            this.$set(this.tableData, i, this.form);
                            return;
                        }
                    }
                }
            },

            handleChange(val) {
                if(this.expectation.salary_min > this.expectation.salary_max){
                    this.errorVisible = true
                    this.error = '最低工资不能高于最高工资'
                }else{
                    this.errorVisible = false
                    this.error = ''
                }
            },
            dealChange (value) {
                // code转汉字大对象
                this.expectation.province = value[0]
                this.expectation.city = value[1]
                // this.expectation.city = CodeToText[value[1]]
            },

            getResumeInfo() {
                this.resumeId = cookie.getCookie('resumeId');

                getUserResume(
                    this.resumeId
                ).then((response) => {
                    this.userResume = response.data
                    this.cropImg = this.userResume.portrait
                }).catch(function (error) {
                    console.log(error);
                });
            },

            getExpectation(){
                this.expectation['resume_id'] = this.resumeId
                const that = this
                getExpectation(
                    this.resumeId
                ).then((response) => {
                    //箭头函数中的this是这个vue对象
                    this.expectation = response.data
                    // this.selectedOptions.push(this.expectation.province)
                    // this.selectedOptions.push(this.expectation.city)
                    this.selectedOptions = [this.expectation.province,this.expectation.city]
                }).catch(function (error) {
                    // 判断是否是新建  function中的this是这个函数作用域
                    if(error.detail.includes("Not found.")){
                        console.log(that)
                        that.createFlag = true
                    }
                });
            },

            createOrUpdateExpect(formName){

              if(this.createFlag){
                  this.createExpectation(formName)
              }else {
                  this.updateExpectation(formName)
              }
            },

            updateExpectation(formName){
                this.$refs[formName].validate((valid) => {
                    if(valid){
                        updateExpectation(
                            this.resumeId,
                            this.expectation
                        ).then((response)=>{
                        }).catch(function (error) {
                            console.log(error)
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                })
            },

            createExpectation(formName){
                this.$refs[formName].validate((valid) => {
                    if(valid){
                        this.expectation.resume_id = this.resumeId
                        createExpectation(
                            this.expectation
                        ).then((response)=>{
                            this.createFlag = false
                        }).catch(function (error) {
                            // console.log(error)
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                })
            },

            updateUserResume(formName){
                this.$refs[formName].validate((valid) => {
                    if(valid){
                        //调用
                        const formData = new FormData();
                        // 等同于使用map.entries()
                        for (let key in this.userResume) {
                            formData.append(key,this.userResume[key])
                        }

                        if(this.imgSrc===''){
                            formData.delete('portrait');
                        }else {
                            let portrait = this.imgSrc?this.imgSrc:this.cropImg
                            this.dataURLtoFile(portrait, this.file.name);
                            formData.set('portrait',this.file);
                        }
                        updateUserResume(
                            this.resumeId,
                            formData
                        ).then((response)=>{
                        }).catch(function (error) {
                            console.log(error)
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                })

            },

            createEdu(){
                this.$refs.edu.createEducation()
            },
            saveEdu(){
                this.$refs.edu.saveEducations()
            },
            saveWork(){
                this.$refs.work.saveWorkExperience()
            },
            createWork(){
                this.$refs.work.createWorkExperience()
            },
            saveProject(){
                this.$refs.project.saveProjectExperience()
            },
            createProject(){
                this.$refs.project.createProjectExperience()
            },
            createSkill(){
                this.$refs.skill.createOrUpdate = 'create'
                this.$refs.skill.createVisible = true
            },
            getSelfAppraise(){
                getSelfAppraise(
                    this.resumeId
                ).then((response)=>{
                    this.textarea = response.data.self_desc
                }).catch(function (error) {
                })
            },
            updateSelfAppraise(){
                updateSelfAppraise(
                    this.resumeId,
                    {
                        resume_id:this.resumeId,
                        self_desc:this.textarea
                    }
                ).then((response)=>{
                    this.textarea = response.data.self_desc
                }).catch(function (error) {

                })
            },

            back(){
                this.$router.push({ path: '../myResume', params: { }})
            },
            saveAll(){
                //  基本信息
                this.updateUserResume('userResume')
                // 求职期望
                this.createOrUpdateExpect('expectation')
                // 教育背景
                this.saveEdu()
                // 工作经历
                this.saveWork()
                // 项目经验
                this.saveProject()
                // 技能特长(不需要，只能在Skills中更新)
                // 自我评价
                this.updateSelfAppraise()
                // 成功提示
                this.successMessage()
            },

            successMessage() {
                this.$message({
                    message: '恭喜你，这是一条成功消息',
                    type: 'success'
                });
            },

            handleClose(done) {
                this.$confirm('确认关闭？')
                    .then(_ => {
                        done();
                    })
                    .catch(_ => {});
            },
            setImage(e) {
                const file = e.target.files[0];
                this.file = file
                if (!file.type.includes('image/')) {
                    return;
                }
                const reader = new FileReader();
                reader.onload = (event) => {
                    this.dialogVisible = true;
                    this.imgSrc = event.target.result;
                    this.$refs.cropper && this.$refs.cropper.replace(event.target.result);
                };
                reader.readAsDataURL(file);
            },
            cropImage() {
                this.cropImg = this.$refs.cropper.getCroppedCanvas().toDataURL();
            },
            cancelCrop() {
                this.dialogVisible = false;
                this.cropImg = this.defaultSrc;
            },
            imageuploaded(res) {
            },
            handleError() {
                this.$notify.error({
                    title: '上传失败',
                    message: '图片上传接口上传失败，可更改为自己的服务器接口'
                });
            },
            //将base64转换为文件
            dataURLtoFile: function(dataurl, filename) {
                var arr = dataurl.split(','),
                    mime = arr[0].match(/:(.*?);/)[1],
                    bstr = atob(arr[1]),
                    n = bstr.length,
                    u8arr = new Uint8Array(n);
                while (n--) {
                    u8arr[n] = bstr.charCodeAt(n);
                }
                return new File([u8arr], filename, { type: mime });
            },

        },
        computed: {
            classification() {
                return Object.keys(this.dutyTimeChoice)
            }
        },
        components: {
            'Education': Education,
            'WorkExperience': WorkExperience,
            'ProjectExperience': ProjectExperience,
            'Skills': Skills,
            'SelfAppraise': SelfAppraise,
            VueCropper
        },
        created() {

        },
        activated() {

        },
        mounted() {
            this.cropImg = this.defaultSrc;
            this.getResumeInfo()
            this.getExpectation()
            this.getSelfAppraise()
        }
    }
</script>
<style scoped>
    .tform {
        font-family: "16px Medium", "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
        font-size: 16px;
    }

    /*.align-center{*/
    /*    margin:0 auto;		!* 居中 这个是必须的，，其它的属性非必须 *!*/
    /*}*/

    .box-card-left {
        border: none;
        display: block;
    }

    .text {
        font-size: 20px;
    }

    .handle-create {
        float: right;
    }
    .message-title {
        cursor: pointer;
    }

    .handle-row {
        margin-top: 30px;
    }

    .content-title {
        font-weight: 400;
        line-height: 50px;
        margin: 10px 0;
        font-size: 22px;
        color: #1f2f3d;
    }

    .pre-img {
        width: 100px;
        height: 100px;
        background: #f8f8f8;
        border: 1px solid #eee;
        border-radius: 5px;
    }

    .crop-demo {
        display: flex;
        align-items: flex-end;
    }

    .crop-demo-btn {
        position: relative;
        width: 100px;
        height: 40px;
        line-height: 40px;
        padding: 0 20px;
        margin-left: 30px;
        background-color: #409eff;
        color: #fff;
        font-size: 14px;
        border-radius: 4px;
        box-sizing: border-box;
    }

    .crop-input {
        position: absolute;
        width: 100px;
        height: 40px;
        left: 0;
        top: 0;
        opacity: 0;
        cursor: pointer;
    }

</style>
