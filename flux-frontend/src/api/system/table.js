import request from '@/utils/request'

// 查询表列
export function listColumn(query) {
  return request({
    url: '/system/table/column/list',
    method: 'get',
    params: query
  })
}

// 更新表列信息
export function editColumnItem(query) {
    return request({
        url: '/system/table/column/edit',
        method: 'put',
        params: query
    })
}

  // 更新表列顺序
export function modifySort(query) {
    return request({
      url: '/system/table/column/sort',
      method: 'post',
      params: query
    })
  }