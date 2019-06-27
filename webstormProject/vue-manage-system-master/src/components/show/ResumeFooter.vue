<template>
    <div class="header">
        <!-- 折叠按钮 -->
        <div class="collapse-btn" @click="collapseChage">
                <el-popover
                        placement="top-start"
                        width="30px"
                        trigger="hover">
                    <el-image
                            style="width: 100px; height: 100px"
                            :src="url"
                            fit="fill"></el-image>
                    <i slot="reference" class="el-icon-s-opportunity"></i>
                </el-popover>
        </div>

        <div class="logo">微信公众号</div>
        <div class="account" style="display: inline-block">
            <ul class="ul">
                <li>
                    GitHub帐号： <el-link :href="github" target="_blank" style="font-size: 22px;color: #fff">{{github}}</el-link>
                </li>
                <li>
                    CSDN博客地址： <el-link :href="csdn" target="_blank" style="font-size: 22px;color: #fff">{{csdn}}</el-link>
                </li>
            </ul>
        </div>

        <div class="address" style="display: inline-block">
            <ul class="ul">
                <li>
                    项目源码： <el-link href="https://github.com/huotong1212/market" target="_blank" style="font-size: 22px;color: #fff">{{github}}</el-link>
                </li>
                <li>
                    项目地址： <el-link :href="csdn" target="_blank" style="font-size: 22px;color: #fff">{{csdn}}</el-link>
                </li>
            </ul>
        </div>


        <div class="header-right">
            <div class="header-user-con">
                <!-- 全屏显示 -->
                <div class="btn-fullscreen" @click="handleFullScreen">
                    <el-tooltip effect="dark" :content="fullscreen?`取消全屏`:`全屏`" placement="bottom">
                        <i class="el-icon-rank"></i>
                    </el-tooltip>
                </div>

                <!-- 用户名下拉菜单 -->
            </div>
        </div>
    </div>
</template>
<script>
    import bus from '../common/bus';
    import cookie from "../static/cookie";
    import {getUser} from "../api/api";

    export default {
        data() {
            return {
                collapse: false,
                fullscreen: false,
                name: 'linxin',
                message: 2,
                userImage: '',
                // url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
                url : require('../../assets/img/qrcode.jpg'),
                todoList: [{
                    title: '今天要修复100个bug',
                    status: false,
                },
                    {
                        title: '今天要修复100个bug',
                        status: false,
                    },
                    {
                        title: '今天要写100行代码加几个bug吧',
                        status: false,
                    },
                ],
                github:'https://github.com/huotong1212',
                csdn:'https://blog.csdn.net/weixin_42142216',
            }
        },
        computed: {
            username() {
                let username = cookie.getCookie('username');
                // let username = localStorage.getItem('ms_username');
                // return username ? username : this.name;
                return username
            }
        },
        methods: {
            // 用户名下拉菜单选择事件
            handleCommand(command) {
                if (command == 'loginout') {
                    // localStorage.removeItem('ms_username')
                    //删除本地存储的用户信息
                    cookie.delCookie('username');
                    cookie.delCookie('token')

                    //删除store的用户信息
                    const loginInfo = {
                        username: '',
                        token: '',
                    }

                    // 更新store数据
                    this.$store.dispatch('setInfo', loginInfo);
                    this.$router.push('/login');
                }
            },
            // 侧边栏折叠
            collapseChage() {
                this.collapse = !this.collapse;
                bus.$emit('collapse', this.collapse);
            },
            // 全屏事件
            handleFullScreen() {
                let element = document.documentElement;
                if (this.fullscreen) {
                    if (document.exitFullscreen) {
                        document.exitFullscreen();
                    } else if (document.webkitCancelFullScreen) {
                        document.webkitCancelFullScreen();
                    } else if (document.mozCancelFullScreen) {
                        document.mozCancelFullScreen();
                    } else if (document.msExitFullscreen) {
                        document.msExitFullscreen();
                    }
                } else {
                    if (element.requestFullscreen) {
                        element.requestFullscreen();
                    } else if (element.webkitRequestFullScreen) {
                        element.webkitRequestFullScreen();
                    } else if (element.mozRequestFullScreen) {
                        element.mozRequestFullScreen();
                    } else if (element.msRequestFullscreen) {
                        // IE11
                        element.msRequestFullscreen();
                    }
                }
                this.fullscreen = !this.fullscreen;
            },
            getUserInfo() {
                getUser().then((response) => {
                    this.userImage = response.data.portrait
                }).catch(function (error) {
                    console.log(error);
                });
            },
        },
        mounted() {
            if (document.body.clientWidth < 1500) {
                this.collapseChage();
            }
            this.getUserInfo()
        },
        activated() {
            this.getUserInfo()
        }
    }
</script>
<style scoped>
    .header {
        position: relative;
        box-sizing: border-box;
        width: 100%;
        height: 70px;
        font-size: 22px;
        position: absolute;
        color: #fff;
        bottom: 0;
    }

    .collapse-btn {
        float: left;
        padding: 0 21px;
        cursor: pointer;
        line-height: 70px;
    }

    .header .logo {
        float: left;
        width: 170px;
        line-height: 70px;
    }

    .header-right {
        float: right;
        padding-right: 50px;
    }

    .header-user-con {
        display: flex;
        height: 70px;
        align-items: center;
    }

    .btn-fullscreen {
        transform: rotate(45deg);
        margin-right: 5px;
        font-size: 24px;
    }

    .btn-bell, .btn-fullscreen {
        position: relative;
        width: 30px;
        height: 30px;
        text-align: center;
        border-radius: 15px;
        cursor: pointer;
    }

    .btn-bell-badge {
        position: absolute;
        right: 0;
        top: -2px;
        width: 8px;
        height: 8px;
        border-radius: 4px;
        background: #f56c6c;
        color: #fff;
    }

    .btn-bell .el-icon-bell {
        color: #fff;
    }

    .user-name {
        margin-left: 10px;
    }

    .user-avator {
        margin-left: 20px;
    }

    .user-avator img {
        display: block;
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }

    .el-dropdown-link {
        color: #fff;
        cursor: pointer;
    }

    .el-dropdown-menu__item {
        text-align: center;
    }

    .account{
        width: 600px;
    }

    .address{
        width: 500px;
    }

    .ul{
        list-style-type: none;
        font-size: 20px;
        position: relative;
    }

    .ul li{
        margin-top: 5px;
    }

</style>
