<template>
  <div style="border-bottom: 1px dashed #cccccc;padding-bottom: 30px;">
    <div class="typeSel">
      <label>试卷类型：</label>
      <el-select label="1213" v-model="programingLanguage" placeholder="请选择试卷类型"
                 @change="getPaperByTypeAndLevel">
        <el-option v-for="item in programingLanguageType" :key="item.value" :label="item.name" :value="item.value">
        </el-option>
      </el-select>
    </div>
    <div class="typeSel">
      <label>等级：</label>
      <el-select v-model="subject" placeholder="请选择等级" @change="getPaperByTypeAndLevel">
        <el-option v-for="item in subjectType" :key="item.value" :label="item.name" :value="item.value">
        </el-option>
      </el-select>
    </div>
    <div>
      <el-button type="primary" @click="jianPage" :disabled="currentPage <= 1">-</el-button>
      <span> {{ this.currentPage }}页 / 共{{ this.allPages }}页</span>
      <el-button type="primary" @click="addPage" :disabled="currentPage >= allPages">+</el-button>
    </div>
  </div>


  <div class="testPaperCenterSty">
    <div class="contentSty">
      <el-card class="box-card" shadow="hover" v-for="(item,index) in allTestPaperData" :key="item.id">
        <p class="title">{{ item.name }}</p>
        <p class="content" style="margin-top: 5px">学科：{{ item.examSubject.name }}</p>
        <p class="content" style="margin-top: 5px">试卷编号：NO.{{ item.id }}</p>
        <p class="content" style="margin-top: 5px">题目数量：{{ item.questionCount }}</p>
        <p class="content" style="margin-top: 5px">试卷总分：{{ item.score }}</p>
        <p class="content" style="margin-top: 5px">建议时长：{{ item.suggestTime }}分钟</p>
        <p class="content" style="margin-top: 5px">发布时间：{{ item.createTime }}</p>

        <p class="content"><span>文件查看下载：</span>
          <el-button text @click="downloadInit(item)">点击查看</el-button>
        </p>


        <div class="tagGroup" style="margin-top: 15px" v-if="item.paperLabels">
          <!-- <el-tag class="tag" type="info" size="mini">{{item.paperLabels}}</el-tag> -->
          <el-tag class="tag" type="success" size="small" v-for="i in item.paperLabels.split(',')" :key="i">{{
              i
            }}
          </el-tag>
          <el-tag class="tag" type="success" size="small" v-if="item.vipAnswer=== 0">免费</el-tag>
          <el-tag class="tag" type="warning" size="small" v-if="item.vipAnswer=== 1">VIP</el-tag>
          <el-tag class="tag" type="danger" size="small" v-if="item.vipAnswer=== 2">VIP</el-tag>
        </div>
      </el-card>
    </div>
  </div>
</template>


<script>

import axios from "axios";

axios.defaults.baseURL = "api/";
export default {
  props: {
    showPopup: {
      type: Number,
      default: 0
    },
  },

  data() {
    return {
      currentPage: 1,
      allPages: 0,
      content: "",
      programingLanguage: "0",
      programingLanguageType: [{
        name: "Scratch/图形化",
        value: "0"
      },
        {
          name: "C/C++",
          value: "1"
        },
        {
          name: "Python",
          value: "2"
        },
        {
          name: "NOIP",
          value: "3"
        },
        {
          name: "机器人技术",
          value: "4"
        },
        {
          name: "科技素养/计算思维",
          value: "5"
        },
        {
          name: "其他",
          value: "99"
        },
      ],
      subject: null,
      subjectType: [{
        name: "全部",
        value: null
      },
        {
          name: "一级",
          value: "1"
        },
        {
          name: "二级",
          value: "2"
        },
        {
          name: "三级",
          value: "3"
        },
        {
          name: "四级",
          value: "4"
        },
        {
          name: "蓝桥杯",
          value: "98"
        },
        {
          name: "NOC/NCT",
          value: "0"
        },
        {
          name: "练习题",
          value: "99"
        }, {
          name: "五级/六级/其他",
          value: "404"
        }
      ],

      allTestPaperData: [],

    }
  },
  watch: {
    programingLanguage: {
      handler: function (n, o) {
        let param = {
          type: this.programingLanguage,
          level: this.subject
        }
        this.$emit("changeSel", param)
      },
      deep: true
    },
    subject: {
      handler: function (n, o) {
        let param = {
          type: this.programingLanguage,
          level: this.subject
        }
        this.$emit("changeSel", param)
      },
      deep: true
    },
  },
  created() {
    this.$message.info("正在模拟登录，请耐心等待");
    this.$message.warning("此操作与网络环境有关");
    console.log('正在模拟登录')
    axios({
      method: "get",
      url: "/login",
    }).then((res) => {
          console.log(res.data);
          if (res.data.code === "0000") {
            // 获取登录数据
            localStorage.setItem("token", res.data.data.token);
            localStorage.setItem("userVipType", res.data.data.userVipType);
            localStorage.setItem("userId", res.data.data.userId);
            localStorage.setItem("username", '17609165208');
            localStorage.setItem("sex", res.data.data.sex)
            localStorage.setItem("agentFlag", res.data.data.agentFlag)
            localStorage.setItem("teacherFlag", res.data.data.teacherFlag)
            // 获取cookie
            this.getAndSetCookie();

          } else {
            this.$message.error(res.data.message);
          }
        }
    )


  },
  methods: {
    getAndSetCookie() {
      axios({
        method: "get",
        url: "/getCookie",
      }).then((res) => {
        console.log(res.data[0].value);
        //   // 获取cookie
        //   设置浏览器Cookie
        this.$cookies.set("JSESSIONID", res.data[0].value);
        console.log("设置cookies成功，当前cookies为"+this.$cookies.get("JSESSIONID"))
        this.$message.success("设置cookies成功,请等待数据加载");
           // 延迟1秒后获取试卷
            setTimeout(() => {
              this.getAll()
            }, 1000);
      })
    },
    addPage() {
      if (this.currentPage < this.allPages) {
        this.currentPage++;
        this.getAll();
      }

    },
    jianPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getAll();
      }

    },
    clickShowType(value) {
      this.$emit("changeShowType", value)
    },

    getPaperByTypeAndLevel() {
      this.loading = true;
      let param = {
        type: this.programingLanguage,
        level: this.subject,
        token: localStorage.getItem("token"),
        JSESSIONID: this.$cookies.get("JSESSIONID")
      };
      axios({
        method: "get",
        url: "/getAll",
        params: param
      }).then((response) => {
        console.log(response.data);

        this.loading = false;
        if (response.data.code === '0000') {
          this.$message.success('查询成功');
          this.allTestPaperData = response.data.data.list;
          this.allPages = response.data.data.pages;
        } else {
          this.$message.error(response.data.message);
        }

      });
    },
    getAll() {
      let param = {
        type: this.programingLanguage,
        level: this.subject,
        token: localStorage.getItem("token"),
        currentPage: this.currentPage,
      };
      axios({
        method: "get",
        url: "/getAll",
        params: param
      }).then((response) => {
        console.log(response.data);
        if (response.data.code === '0000') {
          this.$message.success('查询成功');
          this.allPages = response.data.data.pages;
          this.allTestPaperData = response.data.data.list;
        } else {
          this.$message.error(response.data.message);
        }
      })
    },
    downloadInit(item) {
      console.log("点击查看按钮，试卷名称：" + item.name + "试卷id：" + item.id);
      // 打开新窗口，下载文件
      // 下载地址：'http://www.wancode.net:8010/wancode/exam/pdf/toDownload/'+item.id
      let param = {
        type: this.programingLanguage,
        level: this.subject,
        id: item.id,
        name: item.name,
        token: localStorage.getItem("token"),
        currentPage: this.currentPage,
        JSESSIONID: this.$cookies.get("JSESSIONID")
      };
      axios({
        method: "get",
        url: "/download",
        params: param
      }).then((response) => {
        console.log(response.data);
        if (response.data.code === 200) {
        //   保存成功
          this.$message.success(response.data.name+'已经保存成功');
        }
        else {
          this.$message.error(response.data.message);
        }
      })
      // window.open("http://www.wancode.net:8010/wancode/exam/pdf/toDownload/" + item.id);


    }
    }
  }

</script>

<style scoped>
.box {
  width: 400px;

  .top {
    text-align: center;
  }

  .left {
    float: left;
    width: 60px;
  }

  .right {
    float: right;
    width: 60px;
  }

  .bottom {
    clear: both;
    text-align: center;
  }

  .item {
    margin: 4px;
  }

  .left .el-tooltip__popper,
  .right .el-tooltip__popper {
    padding: 8px 10px;
  }
}

::v-deep.el-radio-button:first-child .el-radio-button__inner {
  border-left: none;
  border-radius: 5px
}

::v-deep.el-radio-button:last-child .el-radio-button__inner {

  border-radius: 5px
}

::v-deep .el-radio-button__inner {
  background: none;
  border: none;
  border-radius: 5px
}

.typeSel {
  display: flex;
  margin-top: 10px;

  p {
    font-size: 18px;
    font-weight: 500;
  }

  .radioGroup {
    margin-left: 20px;
  }
}

.testPaperCenterSty {
  width: 1280px;
  margin-top: 20px;
  min-height: 300px;
  background-color: #FFFFFF;
  position: relative;

  .contentSty {
    padding: 30px 30px;
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    justify-content: flex-start;
    color: #19d3ea;
    font-size: 18px;
    cursor: pointer; /*鼠标悬停变小手*/
  }
}

.box-card {
  width: 380px;
  text-align: left;
  margin-top: 10px;
  margin-left: 20px;

  .title {
    font-size: 18px;
    font-weight: 500;
    line-height: 30px;
    height: 60px;

    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .content {
    font-size: 14px;
    color: #808080;
  }

  .tagGroup {
    .tag {
      margin-left: 10px;
    }

    .tag:first-child {
      margin-left: 0px;
    }
  }
}

</style>
