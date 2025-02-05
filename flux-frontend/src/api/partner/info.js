import request from '@/utils/request'

// 查询合作方列表
export function listInfo(query) {
  return request({
    url: '/partner/info/list',
    method: 'get',
    params: query
  })
}

// 查询合作方详细
export function getInfo(id) {
  return request({
    url: '/partner/info/getById/' + id,
    method: 'get'
  })
}

// 新增合作方
export function addInfo(data) {
  return request({
    url: '/partner/info/add',
    method: 'post',
    data: data
  })
}

// 修改合作方
export function updateInfo(data) {
  return request({
    url: '/partner/info/update',
    method: 'put',
    data: data
  })
}

// 删除合作方
export function delInfo(id) {
  return request({
    url: '/partner/info/delete/' + id,
    method: 'delete'
  })
}