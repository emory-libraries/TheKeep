require File.dirname(__FILE__) + '/abstract_unit'

class DependenciesTest < Test::Unit::TestCase
  
  def teardown
    Dependencies.clear
  end

  def with_loading(*from)
    old_mechanism, Dependencies.mechanism = Dependencies.mechanism, :load
    dir = File.dirname(__FILE__)
    prior_autoload_paths = Dependencies.autoload_paths
    Dependencies.autoload_paths = from.collect { |f| "#{dir}/#{f}" }
    yield
  ensure
    Dependencies.autoload_paths = prior_autoload_paths
    Dependencies.mechanism = old_mechanism
  end

  def test_tracking_loaded_files
    require_dependency(File.dirname(__FILE__) + "/dependencies/service_one")
    require_dependency(File.dirname(__FILE__) + "/dependencies/service_two")
    assert_equal 2, Dependencies.loaded.size
  end

  def test_tracking_identical_loaded_files
    require_dependency(File.dirname(__FILE__) + "/dependencies/service_one")
    require_dependency(File.dirname(__FILE__) + "/dependencies/service_one")
    assert_equal 1, Dependencies.loaded.size
  end

  def test_missing_dependency_raises_missing_source_file
    assert_raises(MissingSourceFile) { require_dependency("missing_service") }
  end

  def test_missing_association_raises_nothing
    assert_nothing_raised { require_association("missing_model") }
  end

  def test_dependency_which_raises_exception_isnt_added_to_loaded_set
    with_loading do
      filename = "#{File.dirname(__FILE__)}/dependencies/raises_exception"
      $raises_exception_load_count = 0

      5.times do |count|
        assert_raises(RuntimeError) { require_dependency filename }
        assert_equal count + 1, $raises_exception_load_count

        assert !Dependencies.loaded.include?(filename)
        assert !Dependencies.history.include?(filename)
      end
    end
  end

  def test_warnings_should_be_enabled_on_first_load
    with_loading do
      old_warnings, Dependencies.warnings_on_first_load = Dependencies.warnings_on_first_load, true

      filename = "#{File.dirname(__FILE__)}/dependencies/check_warnings"
      expanded = File.expand_path(filename)
      $check_warnings_load_count = 0

      assert !Dependencies.loaded.include?(expanded)
      assert !Dependencies.history.include?(expanded)

      silence_warnings { require_dependency filename }
      assert_equal 1, $check_warnings_load_count
      assert_equal true, $checked_verbose, 'On first load warnings should be enabled.'

      assert Dependencies.loaded.include?(expanded)
      Dependencies.clear
      assert !Dependencies.loaded.include?(expanded)
      assert Dependencies.history.include?(expanded)

      silence_warnings { require_dependency filename }
      assert_equal 2, $check_warnings_load_count
      assert_equal nil, $checked_verbose, 'After first load warnings should be left alone.'

      assert Dependencies.loaded.include?(expanded)
      Dependencies.clear
      assert !Dependencies.loaded.include?(expanded)
      assert Dependencies.history.include?(expanded)

      enable_warnings { require_dependency filename }
      assert_equal 3, $check_warnings_load_count
      assert_equal true, $checked_verbose, 'After first load warnings should be left alone.'

      assert Dependencies.loaded.include?(expanded)
    end
  end

  def test_mutual_dependencies_dont_infinite_loop
    with_loading 'dependencies' do
      $mutual_dependencies_count = 0
      assert_nothing_raised { require_dependency 'mutual_one' }
      assert_equal 2, $mutual_dependencies_count

      Dependencies.clear

      $mutual_dependencies_count = 0
      assert_nothing_raised { require_dependency 'mutual_two' }
      assert_equal 2, $mutual_dependencies_count
    end
  end

  def test_as_load_path
    assert_equal '', DependenciesTest.as_load_path
  end

  def test_module_loading
    with_loading 'autoloading_fixtures' do
      assert_kind_of Module, A
      assert_kind_of Class, A::B
      assert_kind_of Class, A::C::D
      assert_kind_of Class, A::C::E::F
    end
  end

  def test_non_existing_const_raises_name_error
    with_loading 'autoloading_fixtures' do
      assert_raises(NameError) { DoesNotExist }
      assert_raises(NameError) { NoModule::DoesNotExist }
      assert_raises(NameError) { A::DoesNotExist }
      assert_raises(NameError) { A::B::DoesNotExist }
    end
  end

  def test_directories_should_manifest_as_modules
    with_loading 'autoloading_fixtures' do
      assert_kind_of Module, ModuleFolder
      Object.send :remove_const, :ModuleFolder
    end
  end

  def test_nested_class_access
    with_loading 'autoloading_fixtures' do
      assert_kind_of Class, ModuleFolder::NestedClass
      Object.send :remove_const, :ModuleFolder
    end
  end

  def test_nested_class_can_access_sibling
    with_loading 'autoloading_fixtures' do
      sibling = ModuleFolder::NestedClass.class_eval "NestedSibling"
      assert defined?(ModuleFolder::NestedSibling)
      assert_equal ModuleFolder::NestedSibling, sibling
      Object.send :remove_const, :ModuleFolder
    end
  end

  def failing_test_access_thru_and_upwards_fails
    with_loading 'autoloading_fixtures' do
      assert ! defined?(ModuleFolder)
      assert_raises(NameError) { ModuleFolder::Object }
      assert_raises(NameError) { ModuleFolder::NestedClass::Object }
      Object.send :remove_const, :ModuleFolder
    end
  end
  
  def test_non_existing_const_raises_name_error_with_fully_qualified_name
    with_loading 'autoloading_fixtures' do
      begin
        A::DoesNotExist.nil?
        flunk "No raise!!"
      rescue NameError => e
        assert_equal "uninitialized constant A::DoesNotExist", e.message
      end
      begin
        A::B::DoesNotExist.nil?
        flunk "No raise!!"
      rescue NameError => e
        assert_equal "uninitialized constant A::B::DoesNotExist", e.message
      end
    end
  end
  
  def test_smart_name_error_strings
    begin
      Object.module_eval "ImaginaryObject"
      flunk "No raise!!"
    rescue NameError => e
      assert e.message.include?("uninitialized constant ImaginaryObject")
    end
  end
  
  def test_autoloadable_constants_for_path_should_handle_empty_autoloads
    assert_equal [], Dependencies.autoloadable_constants_for_path('hello')
  end
  
  def test_autoloadable_constants_for_path_should_handle_relative_paths
    fake_root = 'dependencies'
    relative_root = File.dirname(__FILE__) + '/dependencies'
    ['', '/'].each do |suffix|
      with_loading fake_root + suffix do
        assert_equal ["A::B"], Dependencies.autoloadable_constants_for_path(relative_root + '/a/b')
      end
    end
  end
  
  def test_autoloadable_constants_for_path_should_provide_all_results
    fake_root = '/usr/apps/backpack'
    with_loading fake_root, fake_root + '/lib' do
      root = Dependencies.autoload_paths.first
      assert_equal ["Lib::A::B", "A::B"], Dependencies.autoloadable_constants_for_path(root + '/lib/a/b')
    end
  end
  
  def test_autoloadable_constants_for_path_should_uniq_results
    fake_root = '/usr/apps/backpack/lib'
    with_loading fake_root, fake_root + '/' do
      root = Dependencies.autoload_paths.first
      assert_equal ["A::B"], Dependencies.autoloadable_constants_for_path(root + '/a/b')
    end
  end
  
  def test_qualified_const_defined
    assert Dependencies.qualified_const_defined?("Object")
    assert Dependencies.qualified_const_defined?("::Object")
    assert Dependencies.qualified_const_defined?("::Object::Kernel")
    assert Dependencies.qualified_const_defined?("::Object::Dependencies")
    assert Dependencies.qualified_const_defined?("::Test::Unit::TestCase")
  end
  
  def test_autoloaded?
    with_loading 'autoloading_fixtures' do
      assert ! Dependencies.autoloaded?("ModuleFolder")
      assert ! Dependencies.autoloaded?("ModuleFolder::NestedClass")
      
      assert Dependencies.autoloaded?(ModuleFolder)
      
      assert Dependencies.autoloaded?("ModuleFolder")
      assert ! Dependencies.autoloaded?("ModuleFolder::NestedClass")
      
      assert Dependencies.autoloaded?(ModuleFolder::NestedClass)
      
      assert Dependencies.autoloaded?("ModuleFolder")
      assert Dependencies.autoloaded?("ModuleFolder::NestedClass")
      
      assert Dependencies.autoloaded?("::ModuleFolder")
      assert Dependencies.autoloaded?(:ModuleFolder)
      
      Object.send :remove_const, :ModuleFolder
    end
  end
  
  def test_qualified_name_for
    assert_equal "A", Dependencies.qualified_name_for(Object, :A)
    assert_equal "A", Dependencies.qualified_name_for(:Object, :A)
    assert_equal "A", Dependencies.qualified_name_for("Object", :A)
    assert_equal "A", Dependencies.qualified_name_for("::Object", :A)
    assert_equal "A", Dependencies.qualified_name_for("::Kernel", :A)
    
    assert_equal "Dependencies::A", Dependencies.qualified_name_for(:Dependencies, :A)
    assert_equal "Dependencies::A", Dependencies.qualified_name_for(Dependencies, :A)
  end
  
  def test_file_search
    with_loading 'dependencies' do
      root = Dependencies.autoload_paths.first
      assert_equal nil, Dependencies.search_for_autoload_file('service_three')
      assert_equal nil, Dependencies.search_for_autoload_file('service_three.rb')
      assert_equal root + '/service_one.rb', Dependencies.search_for_autoload_file('service_one')
      assert_equal root + '/service_one.rb', Dependencies.search_for_autoload_file('service_one.rb')
    end
  end
  
  def test_file_search_uses_first_in_autoload_path
    with_loading 'dependencies', 'autoloading_fixtures' do
      deps, autoload = Dependencies.autoload_paths
      assert_match %r/dependencies/, deps
      assert_match %r/autoloading_fixtures/, autoload
      
      assert_equal deps + '/conflict.rb', Dependencies.search_for_autoload_file('conflict')
    end
    with_loading 'autoloading_fixtures', 'dependencies' do
      autoload, deps = Dependencies.autoload_paths
      assert_match %r/dependencies/, deps
      assert_match %r/autoloading_fixtures/, autoload
      
      assert_equal autoload + '/conflict.rb', Dependencies.search_for_autoload_file('conflict')
    end
    
  end
    
  def test_custom_const_missing_should_work
    Object.module_eval <<-end_eval
      module ModuleWithCustomConstMissing
        def self.const_missing(name)
          const_set name, name.to_s.hash
        end

        module A
        end
      end
    end_eval
    
    with_loading 'autoloading_fixtures' do
      assert_kind_of Integer, ::ModuleWithCustomConstMissing::B
      assert_kind_of Module, ::ModuleWithCustomConstMissing::A
      assert_kind_of String, ::ModuleWithCustomConstMissing::A::B
    end
  end
  
  def test_const_missing_should_not_double_load
    with_loading 'autoloading_fixtures' do
      require_dependency '././counting_loader'
      assert_equal 1, $counting_loaded_times
      Dependencies.load_missing_constant Object, :CountingLoader
      assert_equal 1, $counting_loaded_times
    end
  end
  
end
