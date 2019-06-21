<template>
    <div>
        <!--自我评价-->
        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item  v-for="[key,item] in data" :key="key" name="key">
                <template slot="title">
                    <span style="width: 95%">
                        <i class="header-icon el-icon-arrow-right"></i><span class="tform">{{tecnology[key]}}</span>
                    </span>
                    <el-button type="text" icon="el-icon-plus">添加</el-button>
                    <el-button type="text" icon="el-icon-delete">删除</el-button>

                </template>

                <!--Skills-->
                <div class="e-rate" v-for="skill of item">
                    <el-input disabled="true"  placeholder="请输入内容" v-model="skill.skill_desc" style="width: 70%">
                        <template slot="prepend">{{skill.skill_tag}}</template>
                    </el-input>
                    &emsp;&emsp;&emsp;
                    <el-rate disabled="true" class="e-rate" v-model="skill.skill_level" show-text :max=4 :texts="texts">
                    </el-rate>
                    &ensp;&ensp;&ensp;&ensp;
                    <el-button type="text" icon="el-icon-edit" >编辑</el-button>
                    <el-button type="text" icon="el-icon-delete" class="red" >删除</el-button>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
    export default {
        name: "SelfAppraise",
        data:function () {
            return{
                activeNames: ['1'],
            }
        },
        methods:{
            handleChange(val) {
                console.log('this.data',this.data)
                // console.log(this.activeNames)
                // console.log(val);
            }
        },
        computed:{
            data(){
                let data = new Map();
                this.skills.forEach(function (element, index) {
                    // console.log(element); // red green blue
                    // console.log(index);   // 0 1 2

                    // 转为int,因为在Set中的key最好为基础类型，2个不同的对象被认为是2个key
                    let category = Number.parseInt(element.category)

                    // 判断是否被添加过
                    if(!data.has(category)){
                        data.set(category,[])
                    }

                    data.get(category).push(element)
                });
                return data
            },
            rate: {
                get: function () {
                    return function (key) {
                        const levels = new Map([
                            ['1', '了解'],
                            ['2', '熟练'],
                            ['3', '精通'],
                            ['4', '大牛'],
                        ])
                        return levels.get(key)
                    }
                },
                set: function (newValue) {

                }

            },

        }
    }
</script>

<style scoped>
    .tform {
        font-family: "16px Medium","Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
        font-size: 16px;
    }
    .e-rate {
        /*float: left;*/
        display: inline;
    }
</style>
