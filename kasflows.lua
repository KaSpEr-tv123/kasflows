local HttpService = game:GetService("HttpService")

local KasflowsClient = {}
KasflowsClient.__index = KasflowsClient

function KasflowsClient.new(serverUrl)
    local self = setmetatable({}, KasflowsClient)
    self.serverUrl = serverUrl
    self.eventsCallbacks = {
        connect = {},
        disconnect = {},
        messageserver = {},
        messageclient = {}
    }
    self.isConnected = false
    return self
end

function KasflowsClient:on(event, callback)
    if self.eventsCallbacks[event] then
        table.insert(self.eventsCallbacks[event], callback)
    else
        error("Event '" .. event .. "' is not supported")
    end
end

function KasflowsClient:emit(event, data)
    if self.eventsCallbacks[event] then
        for _, callback in ipairs(self.eventsCallbacks[event]) do
            callback(data)
        end
    else
        error("Event '" .. event .. "' is not supported")
    end
end

function KasflowsClient:connect(name, token)
    local success, response = pcall(function()
        return HttpService:PostAsync(self.serverUrl .. "/statusws", HttpService:JSONEncode({
            name = name,
            token = token
        }), Enum.HttpContentType.ApplicationJson)
    end)

    if success then
        local responseData = HttpService:JSONDecode(response)
        if responseData.status == "connected" then
            self.isConnected = true
            self:emit("connect", {
                name = name
            })
            self:startListening(name)
        elseif responseData.status == "already connected" then
            self.isConnected = true
            self:emit("connect", {
                name = name,
                already_connected = true
            })
            self:startListening(name)
        else
            error("Failed to connect: " .. responseData.status)
        end
    else
        error("HTTP request failed while connecting")
    end
end

function KasflowsClient:sendMessage(name, message)
    local success, response = pcall(function()
        return HttpService:PostAsync(self.serverUrl .. "/sendmessage", HttpService:JSONEncode({
            name = name,
            message = message
        }), Enum.HttpContentType.ApplicationJson)
    end)

    if success then
        local responseData = HttpService:JSONDecode(response)
        if responseData.status == "success" then
            self:emit("messageserver", {
                name = name,
                message = message
            })
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
            self:emit("messageclient", {
                name = name,
                message = responseData.message
            })
        elseif responseData.status == "no message" then
            self:emit("messageclient", {
                name = name,
                message = nil
            })
        else
            error("Failed to get message: " .. responseData.status)
        end
    else
        error("HTTP request failed while getting message")
    end
end

function KasflowsClient:startListening(name)
    spawn(function()
        while self.isConnected do
            wait(3) -- Интервал обновления сообщений
            self:getMessage(name)
        end
    end)
end

function KasflowsClient:disconnect()
    self.isConnected = false
    self:emit("disconnect", {})
end

return KasflowsClient
