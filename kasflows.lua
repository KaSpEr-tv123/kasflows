local HttpService = game:GetService("HttpService")

local KasflowsClient = {}
KasflowsClient.__index = KasflowsClient

function KasflowsClient.new(serverUrl)
    local self = setmetatable({}, KasflowsClient)
    self.serverUrl = serverUrl
    self.eventsCallbacks = {}
    self.isConnected = false
    return self
end

function KasflowsClient:on(event, callback)
    if not self.eventsCallbacks[event] then
        self.eventsCallbacks[event] = {}
    end
    table.insert(self.eventsCallbacks[event], callback)
end

function KasflowsClient:off(event, callback)
    if self.eventsCallbacks[event] then
        for i, cb in ipairs(self.eventsCallbacks[event]) do
            if cb == callback then
                table.remove(self.eventsCallbacks[event], i)
                break
            end
        end
    end
end

function KasflowsClient:emit(event, data)
    if self.eventsCallbacks[event] then
        for _, callback in ipairs(self.eventsCallbacks[event]) do
            callback(data)
        end
    end
end

function KasflowsClient:connect(name)
    local success, response = pcall(function()
        return HttpService:PostAsync(self.serverUrl .. "/statusws", HttpService:JSONEncode({
            name = name,
            token = token
        }), Enum.HttpContentType.ApplicationJson)
    end)

    if success then
        local responseData = HttpService:JSONDecode(response)
        if responseData.status == "connected" or responseData.status == "already connected" then
            self.isConnected = true
            self:emit("connect", {
                name = name,
                already_connected = responseData.status == "already connected"
            })
            self:startListening(name)
        else
            error("Failed to connect: " .. responseData.status)
        end
    else
        error("HTTP request failed while connecting")
    end
end

function KasflowsClient:sendMessage(event, data)
    local success, response = pcall(function()
        return HttpService:PostAsync(self.serverUrl .. "/sendmessage", HttpService:JSONEncode({
            event = event,
            data = data
        }), Enum.HttpContentType.ApplicationJson)
    end)

    if success then
        local responseData = HttpService:JSONDecode(response)
        if responseData.status == "success" then
            self:emit(event, data)
        else
            error("Failed to send message: " .. responseData.status)
        end
    else
        error("HTTP request failed while sending message")
    end
end

function KasflowsClient:getMessage(name)
    local success, response = pcall(function()
        return HttpService:PostAsync(self.serverUrl .. "/getmessage", HttpService:JSONEncode({
            name = name
        }), Enum.HttpContentType.ApplicationJson)
    end)

    if success then
        local responseData = HttpService:JSONDecode(response)
        if responseData.status == "success" then
            self:emit(responseData.message.event, responseData.message.data)
        end
    else
        error("HTTP request failed while getting message")
    end
end

function KasflowsClient:start()
    spawn(function()
        while self.isConnected do
            wait()
            self:getMessage(game.Players.LocalPlayer.Name)
        end
    end)
end

function KasflowsClient:disconnect()
    self.isConnected = false
    self:emit("disconnect", {})
end

return KasflowsClient
