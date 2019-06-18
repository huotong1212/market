<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">后台管理系统</div>
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="ruleForm.username" placeholder="username">
                        <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" placeholder="password" v-model="ruleForm.password" @keyup.enter.native="submitForm('ruleForm')">
                        <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                    </el-input>
                </el-form-item>
                <div  style="display: inline">
                    <el-button type="primary" align="left"  @click="submitForm('ruleForm')">登录</el-button>
                    <el-button type="primary" @click="register()">注册</el-button>
                    <el-button type="primary" @click="test()">测试</el-button>
                    &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                    <span class="login-tips"><router-link :to="{ name: 'retrieve' }">忘记密码？</router-link></span>
                </div>
                <p class="login-tips">Tips : 用户名和密码随便填。</p>
            </el-form>
        </div>
    </div>
</template>

<script>
    import { login,getUser,getUserResume } from '../api/api'
    export default {
        data: function(){
            return {
                ruleForm: {
                    username: 'admin',
                    password: '123123'
                },
                rules: {
                    username: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' }
                    ]
                }
            }
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        localStorage.setItem('ms_username',this.ruleForm.username);
                        this.$router.push('/');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            register(){
                console.log('register...')
                // this.$router.push({path:'./register'})
                console.log(this.$router)
                this.$router.push({ path: '../register', params: { userId: '123' }})
            },
            test(){
                // login({
                //     username:'huotong',
                //     password:'879662581',
                // }).then((response)=> {
                //     console.log(response)
                // }).catch(function (error) {
                //     console.log(error);
                // });

                // getUser().then((response)=> {
                //     console.log(response)
                // }).catch(function (error) {
                //     console.log(error);
                // });

                getUserResume({
                    ordering:'-language'
                }).then((response)=> {
                    console.log(response)
                }).catch(function (error) {
                    console.log(error);
                });
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
        color: #fff;
        border-bottom: 1px solid #ddd;
    }
    .ms-login{
        position: absolute;
        left:50%;
        top:50%;
        width:350px;
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
        width:50%;
        height:36px;
        /*margin-bottom: 10px;*/
        text-align: center;
    }
    .login-tips{
        font-size:12px;
        line-height:30px;
        color:#fff;
    }
</style>
