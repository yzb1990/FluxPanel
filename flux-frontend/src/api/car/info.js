import request from '@/utils/request'

// 查询小车信息列表
export function listInfo(query) {
  return request({
    url: '/car/info/list',
    method: 'get',
    params: query
  })
}

// 查询小车信息详细
export function getInfo(id) {
  return request({
    url: '/car/info/getById/' + id,
    method: 'get'
  })
}

// 新增小车信息
export function addInfo(data) {
  return request({
    url: '/car/info/add',
    method: 'post',
    data: data
  })
}

// 修改小车信息
export function updateInfo(data) {
  return request({
    url: '/car/info/update',
    method: 'put',
    data: data
  })
}

// 删除小车信息
export function delInfo(id) {
  return request({
    url: '/car/info/delete/' + id,
    method: 'delete'
  })
}