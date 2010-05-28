class ScannerCamera < ActiveRecord::Base
  has_one :TechImage
  
  
  def self.getDevices
    @devices = find(:all, :select => 'model_name, id', :order => 'model_name')
    
    d = []    
    for device in @devices
      d << [device.model_name, device.id]
    end  
    
    return d
  end  
end
