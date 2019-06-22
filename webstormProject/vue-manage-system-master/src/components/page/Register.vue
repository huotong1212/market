<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">后台管理系统</div>
            <el-card class="box-card box-card-left" style="padding: 30px 30px;" shadow="hover">
                <!--User信息-->
                <div class="form-box align-center" style="margin: 0 auto ;width: 60%">
                    <el-form ref="form" status-icon :rules="rules" :model="form" label-width="80px">
                        <el-form-item label="名称" prop="username">
                            <el-input v-model="form.username" placeholder="请输入名称"></el-input>
                        </el-form-item>
                        <el-form-item label="密码" prop="password">
                            <el-input type="password" placeholder="请输入密码" v-model="form.password">
                            </el-input>
                        </el-form-item>

                        <el-form-item label="性别" prop="gender">
                            <el-radio-group v-model="form.gender">
                                <el-radio label="male" >男</el-radio>
                                <el-radio label="female">女</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="出身日期" prop="birthday">
                            <el-col :span="11">
                                <el-date-picker type="date" value-format="yyyy-MM-dd" placeholder="选择日期" v-model="form.birthday" style="width: 100%;"></el-date-picker>
                            </el-col>
                        </el-form-item>

                        <el-form-item label="手机号" prop="mobile">
                            <el-input v-model="form.mobile"></el-input>
                        </el-form-item>

                        <el-form-item label="验证码" prop="code" style="display: inline-block">
                            <el-input v-model="form.code" style="width: 35%"></el-input>
                            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                            <el-button type="primary" :disabled="flag" @click="sendVerifyCode">{{text}}</el-button>
<!--                            <el-button type="primary" :disabled="flag" @click="setTime">{{text}}</el-button>-->
                        </el-form-item>

                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="form.email"></el-input>
                        </el-form-item>

                        <div class="login-btn">
                            <el-button type="primary" style="width: 85%;float: right" @click="submitForm('form')">注册并登录</el-button>
                        </div>
                    </el-form>
                </div>
            </el-card>

        </div>
    </div>
</template>

<script>
    import customValidate from "../utils/customValidate";
    import {getSMSCode,register} from "../api/api";
    import cookie from "../static/cookie";

    export default {
        data: function(){
            return {
                ruleForm: {
                    username: 'admin',
                    password: '123123'
                },
                rules: {
                    username: [
                        { required: true, message: '请输入用户名', trigger: 'blur' },
                        { min: 2, max: 8, message: '长度在 2 到 8 个字符'}
                    ],
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 6, max: 20, message: '长度在 2 到 20 个字符'}
                    ],
                    mobile:[
                        { required: true, message: '请输入手机号码', trigger: 'blur'},
                        { validator: customValidate.isMobile, trigger: 'blur' }
                    ],
                    email: [
                        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
                        { validator: customValidate.isEmail, trigger: 'blur' }
                    ],
                    code: [
                        { required: true, message: '请输入验证码', trigger: 'blur' },
                        { min: 4, max: 4, message: '长度为 4 个字符'}
                    ],
                    gender: [
                        { required: true, message: '请输入验证码', trigger: 'blur' },
                    ],
                    birthday: [
                        { required: true, message: '请输入出生年月', trigger: 'blur' },
                    ],
                },
                form: {
                    username: '',
                    password:'',
                    mobile: '',
                    email: '',
                    gender: '',
                    birthday: '',
                    code:'',
                },
                text:'获取验证码',
                flag:false,
                countdown : 60
            }
        },
        methods: {
            submitForm(formName) {
                // const formData = new FormData();

                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        console.log('formData',this.form)
                        register(
                            this.form
                        ).then((response) => {
                            console.log('register',response);
                            //本地存储用户信息
                            cookie.setCookie('username', response.data.name, 7);
                            cookie.setCookie('token',response.data.token,7)

                            //存储在store
                            const loginInfo = {
                                username: response.data.name,
                                token: response.data.token
                            }
                            // 更新store数据
                            this.$store.dispatch('setInfo', loginInfo);
                            //跳转到首页页面
                            this.$router.push('/');
                        }).catch(function (error) {
                            console.log(error);
                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            sendVerifyCode(){
                this.$refs.form.validateField('mobile',(errorMessage => {
                    console.log('error',errorMessage)
                    if(errorMessage){
                        return
                    }
                    this.setTime()
                    getSMSCode({
                        mobile:this.form.mobile
                    }).then((response)=>{
                        console.log('SMSCode',response)
                    }).catch(function(error){

                    })

                }))
            },
            setTime() {
                if (this.countdown === 0) {
                    this.flag = false
                    this.text="获取验证码";
                    this.countdown = 60;
                } else {
                    this.flag = true
                    this.text="重新发送(" + this.countdown + ")";
                    this.countdown--;
                    setTimeout(()=>{
                        this.setTime()
                    },1000)
                }
            }
        }
    }
</script>

<style scoped>
    .login-wrap{
        position: relative;
        width:100%;
        height:100%;
        background-image: url(../../assets/img/login-bg.jpg);
        background-size: 100%;
    }
    .ms-title{
        width:100%;
        line-height: 50px;
        text-align: center;
        font-size:20px;
        color: rgba(0, 0, 0, 1);
        border-bottom: 1px solid #ddd;
    }
    .ms-login{
        position: absolute;
        left:40%;
        top:30%;
        width:800px;
        margin:-190px 0 0 -175px;
        border-radius: 5px;
        background: rgba(255,255,255, 0.3);
        overflow: hidden;
    }
    .ms-content{
        padding: 30px 30px;
    }
    .login-btn{
        text-align: center;
    }
    .login-btn button{
        width:100%;
        height:36px;
        margin-bottom: 10px;
    }
    .login-tips{
        font-size:12px;
        line-height:30px;
        color:#fff;
    }
</style>
