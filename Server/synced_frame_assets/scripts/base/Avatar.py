# -*- coding: utf-8 -*-
import KBEngine
import random
import time
import SCDefine
from KBEDebug import *

class Avatar(KBEngine.Proxy):
	"""
	角色实体
	"""
	def __init__(self):
		KBEngine.Proxy.__init__(self)

		self.accountEntity = None
		self.cellData["dbid"] = self.databaseID
		self.nameB = self.cellData["name"]
		
		self._destroyTimer = 0

	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("Avatar[%i-%s] entities enable. entityCall:%s" % (self.id, self.nameB, self.client))
		
		if self._destroyTimer > 0:
			self.delTimer(self._destroyTimer)
			self._destroyTimer = 0

	def onGetCell(self):
		"""
		KBEngine method.
		entity的cell部分实体被创建成功
		"""
		DEBUG_MSG('Avatar::onGetCell: %s' % self.cell)
		
	def createCell(self, space):
		"""
		defined method.
		创建cell实体
		"""
		self.createCellEntity(space)
	
	def destroySelf(self):
		"""
		"""
		if self.client is not None:
			return
			
		if self.cell is not None:
			# 销毁cell实体
			self.destroyCellEntity()
			return
			
		# 如果帐号ENTITY存在 则也通知销毁它
		if self.accountEntity != None:
			if time.time() - self.accountEntity.relogin > 1:
				self.accountEntity.destroy()
			else:
				DEBUG_MSG("Avatar[%i].destroySelf: relogin =%i" % (self.id, time.time() - self.accountEntity.relogin))
				
		# 销毁base
		if not self.isDestroyed:
			self.destroy()

	def destoryCell(self):
		'''
		'''
		DEBUG_MSG("Avatar[%i].destoryCell:"%(self.id))
		if self.cell is not None:
			self.destroyCellEntity()


	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_DESTROY == userArg:
			self.onDestroyTimer()
		
		
	def onClientDeath(self):
		"""
		KBEngine method.
		entity丢失了客户端实体
		"""
		DEBUG_MSG("Avatar[%i].onClientDeath:" % self.id)
		# 防止正在请求创建cell的同时客户端断开了， 我们延时一段时间来执行销毁cell直到销毁base
		# 这段时间内客户端短连接登录则会激活entity
		self._destroyTimer = self.addTimer(10, 0, SCDefine.TIMER_TYPE_DESTROY)
			
	def onClientGetCell(self):
		"""
		KBEngine method.
		客户端已经获得了cell部分实体的相关数据
		"""
		INFO_MSG("Avatar[%i].onClientGetCell:%s" % (self.id, self.client))

	def onDestroyTimer(self):
		DEBUG_MSG("Avatar::onDestroyTimer: %i" % (self.id))
		self.destroySelf()
		
	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)
		
		if self.accountEntity != None:
			self.accountEntity.activeAvatar = None
			self.accountEntity = None



