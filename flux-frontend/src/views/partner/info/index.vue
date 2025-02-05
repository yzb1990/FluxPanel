<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">

            <el-form-item label="合作方名称" prop="partnerName">
              <el-input
                v-model="queryParams.partnerName"
                placeholder="请输入合作方名称"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['partner:info:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['partner:info:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['partner:info:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['partner:info:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="infoList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />



          <el-table-column label="资料介绍" align="center" prop="description" />

          <el-table-column label="id" align="center" prop="id" />

          <el-table-column label="图片" align="center" prop="image" width="100">
            <template #default="scope">
              <image-preview :src="scope.row.image" :width="50" :height="50"/>
            </template>
          </el-table-column>

          <el-table-column label="纬度" align="center" prop="lat" />

          <el-table-column label="经度" align="center" prop="lng" />

          <el-table-column label="所在位置" align="center" prop="location" />

          <el-table-column label="合作方名称" align="center" prop="partnerName" />

          <el-table-column label="价格" align="center" prop="price" />

          <el-table-column label="更新时间" align="center" prop="updateTime" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['partner:info:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['partner:info:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改合作方对话框 -->
    <el-dialog :title="title" v-model="open" width="800px" append-to-body>
      <el-form ref="infoRef" :model="form" :rules="rules" label-width="80px">

                <el-form-item label="资料介绍" prop="description">
                  <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
                </el-form-item>

                <el-form-item label="图片" prop="image">
                  <image-upload v-model="form.image"/>
                </el-form-item>

                <el-form-item label="纬度" prop="lat">
                  <el-input v-model="form.lat" placeholder="请输入纬度" />
                </el-form-item>

                <el-form-item label="经度" prop="lng">
                  <el-input v-model="form.lng" placeholder="请输入经度" />
                </el-form-item>

                <el-form-item label="所在位置" prop="location">
                  <el-input v-model="form.location" placeholder="请输入所在位置" />
                </el-form-item>

                <el-form-item label="合作方名称" prop="partnerName">
                  <el-input v-model="form.partnerName" placeholder="请输入合作方名称" />
                </el-form-item>

                <el-form-item label="价格" prop="price">
                  <el-input v-model="form.price" placeholder="请输入价格" />
                </el-form-item>

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Info">
import { listInfo, getInfo, delInfo, addInfo, updateInfo } from "@/api/partner/info";

const { proxy } = getCurrentInstance();

const infoList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    partnerName: null,
  },
  rules: {
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询合作方列表 */
function getList() {
  loading.value = true;
  listInfo(queryParams.value).then(response => {
    infoList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

// 取消按钮
function cancel() {
  open.value = false;
  reset();
}

// 表单重置
function reset() {
  form.value = {
        createTime: null,        delFlag: null,        description: null,        id: null,        image: null,        lat: null,        lng: null,        location: null,        partnerName: null,        price: null,        updateTime: null  };
  proxy.resetForm("infoRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加合作方";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const partnerInfoId = row.id || ids.value
  getInfo(partnerInfoId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改合作方";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["infoRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateInfo(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addInfo(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _ids = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除合作方编号为"' + _ids + '"的数据项？').then(function() {
    return delInfo(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('partner/info/export', {
    ...queryParams.value
  }, `info_${new Date().getTime()}.xlsx`)
}

getList();
</script>