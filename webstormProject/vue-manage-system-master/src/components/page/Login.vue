<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">后台管理系统</div>
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="ruleForm.username" placeholder="username">
                        <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
                    </el-input>
                    <p class="error-text" v-show="userNameError">{{userNameError}}</p>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" placeholder="password" v-model="ruleForm.password"
                              @keyup.enter.native="login('ruleForm')">
                        <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                    </el-input>
                    <p class="error-text" v-show="parseWordError">{{parseWordError}}</p>
                </el-form-item>
                <div style="display: inline">
                    <p class="error-text" v-show="error">{{error}}</p>
                    <el-button type="primary" align="left" @click="login('ruleForm')">登录</el-button>
                    <el-button type="primary" @click="register()">注册</el-button>
                    <el-button type="primary" @click="login()">测试</el-button>
                    &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                    <span class="login-tips"><router-link :to="{ name: 'retrieve' }">忘记密码？</router-link></span>
                </div>
                <p class="login-tips">Tips : 用户名和密码随便填。</p>
            </el-form>
        </div>
    </div>
</template>

<script>
    import {login, getUser, getUserResume} from '../api/api'
    import cookie from "../static/cookie";

    export default {
        data: function () {
            return {
                ruleForm: {
                    username: 'admin',
                    password: '123123'
                },
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'}
                    ]
                },
                autoLogin: false,
                error: false,
                userNameError: '',
                parseWordError: ''
            }
        },
        methods: {
            login(formName) {
                // 前端表单校验
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let that = this;

                        login({
                            username: this.ruleForm.username, //当前页码
                            password: this.ruleForm.password
                        }).then((response) => {
                            console.log(response);
                            //本地存储用户信息
                            cookie.setCookie('username', this.ruleForm.username, 7);
                            cookie.setCookie('token',response.data.token,7)

                            //存储在store
                            const loginInfo = {
                                username: this.ruleForm.username,
                                token: response.data.token
                            }

                            // 更新store数据
                            this.$store.dispatch('setInfo', loginInfo);
                            //跳转到首页页面
                            this.$router.push('/');
                        })
                            .catch(function (error) {
                                if ("non_field_errors" in error) {
                                    //that.error = error.non_field_errors[0];
                                    that.error = '用户名或密码错误'
                                }
                                if ("username" in error) {
                                    that.userNameError = error.username[0];
                                }
                                if ("password" in error) {
                                    that.parseWordError = error.password[0];
                                }
                            });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        localStorage.setItem('ms_username', this.ruleForm.username);
                        this.$router.push('/');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            register() {
                console.log('register...')
                // this.$router.push({path:'./register'})
                console.log(this.$router)
                this.$router.push({path: '../register', params: {userId: '123'}})
            },
            test() {
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
                    ordering: '-language'
                }).then((response) => {
                    console.log(response)
                }).catch(function (error) {
                    console.log(error);
                });
            }
        },
        activated() {
            this.error = ''
        }
    }
</script>

<style scoped>
    .error-text {
        color: #fa8341;
    }

    .login-wrap {
        position: relative;
        width: 100%;
        height: 100%;
        background-image: url(../../assets/img/login-bg.jpg);
        background-size: 100%;
    }

    .ms-title {
        width: 100%;
        line-height: 50px;
        text-align: center;
        font-size: 20px;
        color: #fff;
        border-bottom: 1px solid #ddd;
    }

    .ms-login {
        position: absolute;
        left: 50%;
        top: 50%;
        width: 350px;
        margin: -190px 0 0 -175px;
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.3);
        overflow: hidden;
    }

    .ms-content {
        padding: 30px 30px;
    }

    .login-btn {
        text-align: center;
    }

    .login-btn button {
        width: 50%;
        height: 36px;
        /*margin-bottom: 10px;*/
        text-align: center;
    }

    .login-tips {
        font-size: 12px;
        line-height: 30px;
        color: #fff;
    }
</style>
