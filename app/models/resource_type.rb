class ResourceType < ActiveRecord::Base
  has_one :Content
  
  def self.getResourceTypes
    @resourcetypes = find(:all, :select => 'resource_type, id', :order => 'resource_type')
    
    types = []    
    for rt in @resourcetypes
      types << [rt.resource_type, rt.id]
    end  
    
    return types
  end
end